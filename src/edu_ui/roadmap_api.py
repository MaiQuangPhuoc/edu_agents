"""Student-scoped learning-path catalog, sessions, and persistent completion."""
import os
import re
import unicodedata
from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, StrictBool
from src.edu_planning.path_store import list_learning_paths, load_learning_path, set_session_completed, ProgressConflict

router = APIRouter(prefix='/api/ui/roadmaps', tags=['roadmap-library'])


def student_id():
    value = os.getenv('EDU_UI_STUDENT_ID', 'hs_002')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', value): raise HTTPException(500, 'Mã học sinh không hợp lệ.')
    return value


def sessions(data):
    return [{**session, 'week_no': week['week_no'], 'session_no': index}
            for week in data.get('weeks', []) for index, session in enumerate(week.get('sessions', []), 1)]


def summary(data):
    items = sessions(data)
    done = sum(s.get('completed') is True for s in items)
    weeks = {w['week_no'] for w in data.get('weeks', []) if w.get('sessions')}
    planned_weeks = data.get('schedule', {}).get('total_weeks', 0) or 0
    complete_scope = bool(planned_weeks) and set(range(1, int(planned_weeks) + 1)) <= weeks
    state = 'not_started' if not done else 'in_progress'
    if items and done == len(items): state = 'completed' if complete_scope else 'window_completed'
    return {k: data.get(k) for k in ['plan_id', 'student_id', 'subject', 'title', 'created_at', 'updated_at', 'progress_version']} | {
        'schedule': data.get('schedule', {}), 'current_phase': data.get('current_phase'),
        'session_count': len(items), 'completed_count': done, 'detailed_weeks': len(weeks),
        'phase_count': len(data.get('outline', [])), 'status': state, 'goal': (data.get('overview') or {}).get('muc_tieu_tong', ''),
        'progress_percent': round(done * 100 / len(items)) if items else 0,
        'fully_detailed': complete_scope}


def public_path(data):
    # Preserve private generation context only on disk/server.
    keys = ['plan_id', 'student_id', 'subject', 'title', 'created_at', 'updated_at', 'progress_version',
            'schedule', 'current_phase', 'outline', 'weeks', 'assumptions', 'overview']
    return {key: data[key] for key in keys if key in data}


def read(plan_id):
    try: data = load_learning_path(student_id(), plan_id)
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc
    except (OSError, ValueError) as exc: raise HTTPException(500, 'Không đọc được JSON lộ trình.') from exc
    if not data: raise HTTPException(404, 'Không tìm thấy lộ trình của học sinh hiện tại.')
    return data


@router.get('')
def catalog(subject: str = '', status: str = '', q: str = '', sort: str = 'newest'):
    try: plans = [summary(p) for p in list_learning_paths(student_id())]
    except (OSError, ValueError) as exc: raise HTTPException(500, 'Không đọc được thư viện lộ trình.') from exc
    subjects = sorted({p.get('subject') or 'Chưa xác định môn' for p in plans})
    if subject: plans = [p for p in plans if (p.get('subject') or 'Chưa xác định môn') == subject]
    if status: plans = [p for p in plans if p['status'] == status]
    def normalized(value): return ''.join(c for c in unicodedata.normalize('NFD', value.casefold().replace('đ', 'd')) if not unicodedata.combining(c))
    if q: plans = [p for p in plans if normalized(q.strip()) in normalized((p.get('title') or '') + ' ' + (p.get('subject') or '') + ' ' + (p.get('goal') or ''))]
    if sort == 'progress': plans.sort(key=lambda p: (p['progress_percent'], p.get('created_at') or ''), reverse=True)
    elif sort == 'start_date': plans.sort(key=lambda p: p['schedule'].get('start_date') or '')
    else: plans.sort(key=lambda p: p.get('created_at') or p['schedule'].get('start_date') or '', reverse=True)
    return {'roadmaps': plans, 'subjects': subjects, 'student_id': student_id(), 'connected': True}


@router.get('/calendar')
def calendar(subject: str = '', status: str = '', date_from: str = '', date_to: str = '', plan_id: str = ''):
    try:
        for value in (date_from, date_to):
            if value: date.fromisoformat(value)
    except ValueError as exc: raise HTTPException(422, 'Khoảng ngày không hợp lệ.') from exc
    if date_from and date_to and date_from > date_to: raise HTTPException(422, 'Ngày bắt đầu phải trước hoặc bằng ngày kết thúc.')
    plans = [read(plan_id)] if plan_id else list_learning_paths(student_id())
    rows = []
    for plan in plans:
        if subject and (plan.get('subject') or 'Chưa xác định môn') != subject: continue
        for session in sessions(plan):
            if status == 'completed' and not session.get('completed'): continue
            if status == 'pending' and session.get('completed'): continue
            session_date = session.get('date') or ''
            if (date_from or date_to) and not session_date: continue
            if date_from and session_date < date_from: continue
            if date_to and session_date > date_to: continue
            rows.append({**session, 'plan_id': plan['plan_id'], 'plan_title': plan.get('title', ''), 'subject': plan.get('subject', ''), 'progress_version': plan.get('progress_version', 0)})
    rows.sort(key=lambda s: (s.get('date') or '9999', s.get('start_time') or '', s['plan_id'], s['session_no']))
    return {'sessions': rows}


@router.post('/from-session/{sid}')
def import_session(sid: str):
    from src.edu_ui.workflow_api import get_session
    from src.edu_planning.path_store import save_learning_path
    session = get_session(sid)
    if session['student_id'] != student_id(): raise HTTPException(404, 'Không tìm thấy phiên học sinh.')
    data = session['state'].get('learning_path')
    if not data: raise HTTPException(404, 'Phiên chưa có lộ trình.')
    if data.get('plan_id') and load_learning_path(student_id(), data['plan_id']): return {'plan_id': data['plan_id']}
    saved = save_learning_path(student_id(), data)
    import json
    session['state']['learning_path'] = json.loads(saved.read_text(encoding='utf-8'))
    return {'plan_id': session['state']['learning_path']['plan_id']}


@router.get('/{plan_id}')
def detail(plan_id: str):
    data = read(plan_id)
    return {'path': public_path(data), 'summary': summary(data)}


class Completion(BaseModel):
    completed: StrictBool
    expected_version: int = Field(ge=0)


@router.put('/{plan_id}/sessions/{session_id}/completion')
def complete_session(plan_id: str, session_id: str, body: Completion):
    try:
        data = set_session_completed(student_id(), plan_id, session_id, body.completed, body.expected_version)
    except ProgressConflict as exc: raise HTTPException(409, str(exc)) from exc
    except (KeyError, FileNotFoundError) as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc
    except OSError as exc: raise HTTPException(500, 'Không lưu được trạng thái buổi học. Vui lòng thử lại.') from exc
    return {'path': public_path(data), 'summary': summary(data)}


@router.post('/{plan_id}/practice-context')
def practice_context(plan_id: str):
    # Reuse the existing real exam generator; no fake exercise button or answer key.
    data = read(plan_id)
    from src.edu_ui.workflow_api import create, Create, get_session
    from src.edu_planning.student_store import load_student_model
    created = create(Create(mode='planning'))
    session = get_session(created['session_id'])
    session['state'] = {'learning_path': data, 'lp_window': {'subject': data.get('subject', '')},
                        'student_model': data.get('student_model_snapshot') or load_student_model(student_id()) or {}, 'roadmap_status': 'path_ready', 'messages': []}
    return created
