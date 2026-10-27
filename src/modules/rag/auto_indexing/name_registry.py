"""Persistent Python-literal registry. Never execute the generated .py file."""
import ast
import os
import pprint
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path

from filelock import FileLock
from .sources import DEFAULT_OUTPUT_ROOT

REGISTRY_PATH = DEFAULT_OUTPUT_ROOT / 'collection_names.py'


class DuplicateCollectionName(ValueError):
    pass


def validate_name(name):
    name = unicodedata.normalize('NFC', str(name)).strip()
    if not name or len(name) > 200 or any(ord(c) < 32 or c in '/\\' for c in name):
        raise ValueError('Tên sách/tài liệu phải có 1–200 ký tự, không chứa dấu /, \\ hoặc ký tự điều khiển.')
    return name


def _read(path):
    if not path.exists():
        return {}
    tree = ast.parse(path.read_text(encoding='utf-8'))
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Assign):
        raise ValueError('File collection_names.py không đúng định dạng; không tự ghi đè.')
    assignment = tree.body[0]
    if len(assignment.targets) != 1 or not isinstance(assignment.targets[0], ast.Name) or assignment.targets[0].id != 'COLLECTION_NAMES':
        raise ValueError('Thiếu COLLECTION_NAMES trong file đăng ký.')
    data = ast.literal_eval(assignment.value)
    if not isinstance(data, dict):
        raise ValueError('COLLECTION_NAMES phải là dictionary.')
    return data


def _write(path, data):
    temp = path.with_name(f'{path.name}.{uuid.uuid4().hex}.tmp')
    temp.write_text('# Tự động ghi; chỉ đọc bằng ast.literal_eval, không import/exec.\nCOLLECTION_NAMES = '
                    + pprint.pformat(data, sort_dicts=True, width=100) + '\n', encoding='utf-8')
    os.replace(temp, path)


def update_registry(name, *, reserve=False, registry_path=None, **details):
    name = validate_name(name)
    path = Path(registry_path or REGISTRY_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with FileLock(str(path) + '.lock', timeout=30):
        data = _read(path)
        key = name.casefold()
        if reserve and key in data:
            raise DuplicateCollectionName(f'Collection "{name}" đã được sử dụng. Hãy nhập tên khác.')
        if not reserve and key not in data:
            raise ValueError('Collection chưa được đăng ký.')
        data[key] = {**data.get(key, {}), 'collection_name': name, **details,
                     'updated_at': datetime.now(timezone.utc).isoformat()}
        _write(path, data)
    return path
