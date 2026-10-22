"""Chia giáo án Markdown thành các block JSON, không cần LLM.

Cài đặt: pip install pyyaml
Chạy: python chunk_markdown.py ./toan_10
Hoặc: python chunk_markdown.py ./chapter_I.md -o ./toan_10_chunks

Cấu trúc: YAML đầu file; ## PHẦN A/B; ### A.n/BÀI; #### 1–6.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml


def clean(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def sections(text, level):
    pattern = rf"^{'#' * level} (.+)$"
    matches = list(re.finditer(pattern, text, re.M))
    return [
        (m.group(1), text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)])
        for i, m in enumerate(matches)
    ]


def split_blocks(text, max_chars):
    """Giới hạn mềm theo ký tự; giữ nguyên đoạn, bảng, code và công thức khối."""
    units, lines = [], []
    fence = False
    math = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('```'):
            fence = not fence
        if not fence:
            if stripped.count('$$') % 2:
                math = not math
            if r'\[' in stripped and r'\]' not in stripped:
                math = True
            if r'\]' in stripped:
                math = False
        if not stripped and not fence and not math:
            if lines:
                units.append('\n'.join(lines))
                lines = []
        else:
            lines.append(line)
    if lines:
        units.append('\n'.join(lines))
    blocks, current = [], ''
    for unit in units:
        candidate = current + '\n\n' + unit if current else unit
        if current and len(candidate) > max_chars:
            blocks.append(current)
            current = unit
        else:
            current = candidate
    if current:
        blocks.append(current)
    return blocks


def lesson_metadata(body, heading):
    info = next((text for title, text in sections(body, 4) if title.startswith('1.')), '')
    plain = info.replace('`', '').replace('*', '')
    marker = re.search(r'<!--\s*lesson_id:\s*([^;\s>]+)', body)
    lesson_id = marker.group(1) if marker else None
    if lesson_id == 'null':
        lesson_id = None
    title_match = re.search(r'lesson_title\s*:\s*`([^`]+)`', info)
    title = title_match.group(1) if title_match else re.sub(r'^(?:BÀI\s+\d+\.|ÔN TẬP\.)\s*', '', heading)
    result = {'lesson_id': lesson_id, 'lesson_title': title}
    for key, label in [('official_periods', None), ('suggested_sessions', r'Số buổi tự học đề xuất'), ('minutes_per_session', r'(?:Thời lượng[^:\n]*|mỗi buổi)')]:
        match = re.search(rf'{key}\s*:\s*(null|\d+)', plain)
        if not match and label:
            match = re.search(rf'{label}\s*:?\s*(\d+)', plain, re.I)
        result[key] = int(match.group(1)) if match and match.group(1) != 'null' else None
    sources = re.search(r'source_ids\s*:\s*`([^`]+)`', info)
    if sources:
        result['source_ids'] = [s.strip() for s in sources.group(1).split(',')]
    return result


def chunk_file(path, max_chars=2400):
    original = path.read_text(encoding='utf-8-sig')
    front = re.match(r'\A---\s*\n(.*?)\n---\s*\n', original, re.S)
    if not front:
        raise ValueError(f'{path.name}: thiếu YAML đầu file')
    common = yaml.safe_load(front.group(1))
    for key in ['document_id', 'document_type', 'subject', 'grade', 'textbook_series', 'chapter_id']:
        if key not in common:
            raise ValueError(f'{path.name}: thiếu {key}')
    body = original[front.end():]
    # Hỗ trợ marker lesson_id đặt trước heading bài ở các chương khác.
    body = re.sub(r'(<!--\s*lesson_id:[^>]*-->)\s*\n(### [^\n]+)', r'\2\n\1', body)
    chunks = []
    source_hash = hashlib.sha256(original.encode('utf-8')).hexdigest()
    summary_types = ['chapter_objectives', 'lesson_list', 'key_knowledge', 'prerequisites', 'time_plan']
    detail_types = ['lesson_info', 'objectives', 'must_know', 'must_understand', 'activity', 'assessment']

    def add(text, metadata, headings):
        blocks = (
            [clean(text)]
            if metadata['content_type'] == 'detail'
            else split_blocks(clean(text), max_chars)
        )

        for part_index, block in enumerate(blocks, 1):
            index = len(chunks) + 1
            data = {**metadata, 'chunk_id': f"{common['document_id']}_{common['document_type']}_{index:03d}",
                    'chunk_index': index, 'part_index': part_index, 'heading_path': headings,
                    'source_file': path.name, 'source_sha256': source_hash}
            chunks.append({'content': ' > '.join(headings) + '\n\n' + block, 'metadata': data})

    for part_title, part_body in sections(body, 2):
        if 'PHẦN A.' in part_title:
            for title, text in sections(part_body, 3):
                number = re.match(r'A\.(\d+)\.', title)
                section_type = summary_types[int(number.group(1)) - 1] if number and 1 <= int(number.group(1)) <= 5 else 'chapter_overview'
                add(text, {**common, 'content_type': 'summary', 'lesson_id': None, 'lesson_title': None,
                           'section_types': [section_type], 'time_scope': 'chapter'},
                    [common.get('chapter_title', common['chapter_id']), title])
        elif 'PHẦN B.' in part_title:
            for lesson_title, lesson_body in sections(part_body, 3):
                lesson = lesson_metadata(lesson_body, lesson_title)

                items = {}
                for title, text in sections(lesson_body, 4):
                    match = re.match(r'(\d+)\.', title)
                    if match:
                        items[int(match.group(1))] = (title, text)

                # Một bài: 4 nhóm chunk — (1, 2), (3), (4), (5, 6)
                for group in [(1, 2), (3,), (4,), (5, 6)]:
                    selected = [
                        (n, *items[n]) for n in group if n in items
                    ]
                    if not selected:
                        continue

                    text = '\n\n'.join(
                        f'{title}\n\n{clean(body)}'
                        for _, title, body in selected
                    )
                    types = [
                        detail_types[n - 1] for n, _, _ in selected
                    ]
                    group_title = ' + '.join(
                        title for _, title, _ in selected
                    )

                    add(
                        text,
                        {
                            **common,
                            **lesson,
                            'content_type': 'detail',
                            'section_types': types,
                            'time_scope': 'lesson',
                        },
                        [
                            common.get('chapter_title', common['chapter_id']),
                            lesson_title,
                            group_title,
                        ],
                    )

    if not any(c['metadata']['content_type'] == 'summary' for c in chunks) or not any(c['metadata']['content_type'] == 'detail' for c in chunks):
        raise ValueError(f'{path.name}: không tìm đủ PHẦN A/B theo cấu trúc chuẩn')
    # Giữ nguyên nguồn và ghi chú cuối file ngoài các chunk kiến thức.
    extras = {title: clean(text) for title, text in sections(body, 2) if 'PHẦN A.' not in title and 'PHẦN B.' not in title}
    return {'document_metadata': common, 'source_file': path.name, 'source_sha256': source_hash,
            'max_chars_soft_limit': max_chars, 'total_chunks': len(chunks), 'chunks': chunks, 'appendices': extras}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Một file .md hoặc thư mục chứa .md')
    parser.add_argument('-o', '--output', type=Path, default=Path('toan_10_chunks'))
    parser.add_argument('--max-chars', type=int, default=2400, help='Giới hạn mềm theo ký tự, không phải token')
    args = parser.parse_args()
    if args.max_chars < 1:
        parser.error('--max-chars phải lớn hơn 0')
    files = [args.input] if args.input.is_file() else sorted(args.input.glob('*.md'))
    if not files:
        parser.error('Không tìm thấy file Markdown')
    args.output.mkdir(parents=True, exist_ok=True)
    for path in files:
        result = chunk_file(path, args.max_chars)
        output = args.output / f'{path.stem}.json'
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'{path.name} -> {output}: {result["total_chunks"]} chunks')


if __name__ == '__main__':
    main()

    # python src/modules/rag/process_toan_10/chunk_markdown_giao_an.py --% src/modules/documents/lesson_plans/chan_troi_sang_tao/toan_10 -o src/modules/documents/lesson_plans/chan_troi_sang_tao/toan_10_chunks
