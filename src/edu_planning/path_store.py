"""Timestamp-named learning paths; keeps the legacy latest-per-student mirror."""
import copy
import hashlib
import json
import logging
import os
from contextlib import contextmanager
import re
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from src.edu_planning.student_store import STUDENT_DIR
from datetime import datetime

PATH_DIR = STUDENT_DIR.parent / 'learning_path'
LOCK = threading.RLock()  # UI runs with one worker; protects concurrent thread writes.
logger = logging.getLogger(__name__)

class ProgressConflict(ValueError):
    pass


@contextmanager
def _transaction():
    # Lock across UI threads and a separate planning CLI process. A crash releases
    # the OS lock automatically; the archive JSON is still replaced atomically.
    with LOCK:
        PATH_DIR.mkdir(parents=True, exist_ok=True)
        with (PATH_DIR / '.library.lock').open('a+b') as handle:
            if os.name == 'nt':
                import msvcrt
                if os.fstat(handle.fileno()).st_size == 0:
                    handle.write(b'0'); handle.flush()
                handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if os.name == 'nt':
                    handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _student(student_id):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', student_id):
        raise ValueError('Mã học sinh không hợp lệ.')
    return student_id


def _plan_id(plan_id):
    try: return str(uuid.UUID(str(plan_id)))
    except (ValueError, TypeError, AttributeError) as exc: raise ValueError('Mã lộ trình không hợp lệ.') from exc


def _archive(student_id, plan_id):
    directory = PATH_DIR / 'library' / _student(student_id)
    pid = _plan_id(plan_id)
    legacy = directory / (pid + '.json')
    if legacy.exists(): return legacy
    for path in directory.rglob('*.json') if directory.exists() else []:
        try:
            data = _read(path)
            if data.get('student_id') == student_id and data.get('plan_id') == pid:
                return path
        except (OSError, ValueError, AttributeError):
            continue
    return legacy


def _new_archive(student_id):
    # Local server time; day directory prevents equal times on different days.
    now = datetime.now().astimezone()
    directory = PATH_DIR / 'library' / _student(student_id) / now.strftime('%Y-%m-%d')
    stem = now.strftime('%H-%M-%S')
    target = directory / (stem + '.json')
    counter = 2
    while target.exists():
        target = directory / f'{stem}_{counter}.json'
        counter += 1
    return target


def _read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def _markdown(path, data):
    try:
        from src.edu_planning.path_format import to_markdown
        path.with_suffix('.md').write_text(to_markdown(data), encoding='utf-8')
    except Exception:
        logger.warning('JSON saved; Markdown mirror could not be refreshed: %s', path, exc_info=True)


def infer_subject(data):
    metadata = data.get('metadata') if isinstance(data.get('metadata'), dict) else {}
    explicit = data.get('subject') or data.get('mon_hoc') or metadata.get('subject')
    if isinstance(explicit, str) and explicit.strip(): return explicit.strip()
    # Older files can be identified only when all lesson titles match one curriculum.
    lessons = {s.get('lesson') for w in data.get('weeks', []) for s in w.get('sessions', []) if s.get('lesson')}
    if not lessons: return ''
    source = Path(__file__).resolve().parents[1] / 'modules' / 'documents' / 'curriculum_sections.json'
    try:
        curriculum = _read(source)
        candidates = [subject for subject, chapters in curriculum.items()
                      if lessons <= {lesson for chapter in chapters.values() for lesson in chapter.get('lessons', {})}]
        return candidates[0] if len(candidates) == 1 else ''
    except (OSError, ValueError, TypeError, AttributeError): return ''


def _prepare(student_id, lp, *, legacy=False):
    if not isinstance(lp, dict) or not isinstance(lp.get('weeks'), list) or not isinstance(lp.get('schedule'), dict):
        raise ValueError('JSON không đúng cấu trúc LearningPath.')
    if any(not isinstance(w, dict) or 'week_no' not in w or not isinstance(w.get('sessions', []), list) or any(not isinstance(s, dict) for s in w.get('sessions', [])) for w in lp['weeks']):
        raise ValueError('Dữ liệu tuần hoặc buổi học không hợp lệ.')
    data = copy.deepcopy(lp)
    if data.get('plan_id'):
        pid = _plan_id(data['plan_id'])
    elif legacy:
        digest = hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        pid = str(uuid.uuid5(uuid.NAMESPACE_URL, 'eduagent:legacy:' + student_id + ':' + digest))
    else: pid = str(uuid.uuid4())
    data.update(plan_id=pid, student_id=_student(student_id))
    data['subject'] = infer_subject(data)
    data.setdefault('created_at', None if legacy else _now())
    data.setdefault('updated_at', data['created_at'])
    data.setdefault('progress_version', 0)
    data.setdefault('title', f"{data['subject'] or 'Lộ trình học'} · {data['schedule'].get('start_date', '')}")
    session_ids = set()
    for week in data['weeks']:
        for index, session in enumerate(week.get('sessions', []), 1):
            if not isinstance(session.get('session_id'), str) or not session['session_id'] or session['session_id'] in session_ids:
                session['session_id'] = str(uuid.uuid5(uuid.UUID(pid), f"{week['week_no']}:{index}:{session.get('date', '')}:{session.get('lesson', '')}"))
            session_ids.add(session['session_id'])
            session['completed'] = session.get('completed') is True
            session.setdefault('completed_at', None)
            if not session['completed']: session['completed_at'] = None
    return data


def _migrate(student_id):
    """Import only this student's legacy files; archives are authoritative."""
    if not PATH_DIR.exists(): return
    for path in PATH_DIR.glob('*.json'):
        try:
            raw = _read(path)
            if not isinstance(raw, dict): continue
            if path.stem != student_id and raw.get('student_id') != student_id: continue
            data = _prepare(student_id, raw, legacy=True)
            target = _archive(student_id, data['plan_id'])
            if not target.exists(): _write(_new_archive(student_id), data)
            if path.stem == student_id and not raw.get('plan_id'):
                _write(path, data)
        except (OSError, ValueError, KeyError, TypeError):
            logger.warning('Skipped invalid legacy path file: %s', path, exc_info=True)


def save_learning_path(student_id: str, lp: dict) -> Path:
    student_id = _student(student_id)
    with _transaction():
        _migrate(student_id)  # Preserve the previous latest before replacing it.
        data = _prepare(student_id, lp)
        target = _archive(student_id, data['plan_id'])
        if target.exists():
            # Never silently overwrite an existing plan or erase its study progress.
            raise ValueError('ID lộ trình đã tồn tại. Lưu lần sinh mới bằng một ID mới.')
        target = _new_archive(student_id)
        _write(target, data)
        _write(PATH_DIR / f'{student_id}.json', data)
        _markdown(target, data)
        _markdown(PATH_DIR / f'{student_id}.json', data)
        return target


def list_learning_paths(student_id):
    student_id = _student(student_id)
    with _transaction():
        _migrate(student_id)
        directory = PATH_DIR / 'library' / student_id
        result = []
        for path in directory.rglob('*.json') if directory.exists() else []:
            try:
                data = _read(path)
                if isinstance(data, dict) and data.get('student_id') == student_id: result.append(_prepare(student_id, data, legacy=True))
            except (OSError, ValueError, AttributeError, KeyError, TypeError): logger.warning('Cannot read archived path: %s', path)
        return result


def load_learning_path(student_id: str, plan_id: Optional[str] = None) -> Optional[dict]:
    student_id = _student(student_id)
    with _transaction():
        if plan_id:
            path = _archive(student_id, plan_id)
        else:
            path = PATH_DIR / f'{student_id}.json'
        if not path.exists(): return None
        return _read(path)


def set_session_completed(student_id, plan_id, session_id, completed, expected_version):
    with _transaction():
        path = _archive(student_id, plan_id)
        if not path.exists(): raise FileNotFoundError('Không tìm thấy lộ trình.')
        data = _read(path)
        session = next((s for w in data['weeks'] for s in w.get('sessions', []) if s.get('session_id') == session_id), None)
        if session is None: raise KeyError('Không tìm thấy buổi học.')
        if bool(session.get('completed')) == completed: return data
        if data.get('progress_version', 0) != expected_version:
            raise ProgressConflict('Tiến độ đã thay đổi ở cửa sổ khác. Đã tải lại dữ liệu; hãy thử lại.')
        session['completed'] = completed
        session['completed_at'] = _now() if completed else None
        data['progress_version'] = data.get('progress_version', 0) + 1
        data['updated_at'] = _now()
        _write(path, data)
        latest = PATH_DIR / f'{student_id}.json'
        if latest.exists():
            try:
                if _read(latest).get('plan_id') == data['plan_id']: _write(latest, data)
            except (OSError, ValueError): logger.warning('Progress saved to archive; latest mirror was not updated', exc_info=True)
        return data
