import re
from pathlib import Path
import json

def split_chapters(filepath: str) -> list[dict]:
    text = Path(filepath).read_text(encoding='utf-8')
    
    RE_CH = re.compile(r'^Chương ([IVXLC]+)\s+(.+)$', re.MULTILINE)
    matches = list(RE_CH.finditer(text))
    
    chapters = []
    for i, m in enumerate(matches):
        start = m.start()
        end   = matches[i+1].start() if i+1 < len(matches) else len(text)
        chapters.append({
            'chapter_id'  : m.group(1),
            'chapter_name': m.group(2).strip(),
            'text'        : text[start:end]
        })
    return chapters

LATEX_MAP = {
    r'\forall':'∀', r'\exists':'∃', r'\in':'∈', r'\notin':'∉',
    r'\subset':'⊂', r'\cup':'∪', r'\cap':'∩', r'\emptyset':'∅',
    r'\leq':'≤', r'\geq':'≥', r'\neq':'≠', r'\infty':'∞',
    r'\Rightarrow':'⇒', r'\Leftrightarrow':'⟺',
    r'\mathbb{R}':'ℝ', r'\mathbb{N}':'ℕ', r'\mathbb{Z}':'ℤ',
    r'\sqrt':'√', r'\pi':'π', r'\pm':'±', r'\times':'×',
}

def norm(text):
    for k, v in LATEX_MAP.items():
        text = text.replace(k, v)
    # Bỏ $...$ wrapper
    text = re.sub(r'\$\$?([^$]+)\$?\$', lambda m: m.group(1), text)
    # \{ \} → { }
    text = text.replace(r'\{', '{').replace(r'\}', '}')
    # x^2 → x² (optional)
    text = re.sub(r'\^(\d)', lambda m: '⁰¹²³⁴⁵⁶⁷⁸⁹'[int(m.group(1))], text)
    # Còn lại \command{...} → content
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    # Lone \command → bỏ
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # Fix double space sinh ra sau khi xóa
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'== \d+ ==', '', text)
    # Fix các từ dính nhau thường gặp
    text = re.sub(r'([a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ])([A-ZÁÀẢÃẠ])', r'\1 \2', text)
    return text.strip()

CHAPTER_TYPE = {
    'I'  : 'Đại số',
    'II' : 'Đại số',
    'III': 'Đại số',
    'IV' : 'Hình học',
    'V'  : 'Hình học',
    'VI' : 'Thống kê',
}

def check_has_table(text: str) -> bool:
    return bool(re.search(r'-+\s*\|\s*-+', text))

def make_chapter_chunk(chapter: dict) -> dict:
    ch_id   = chapter['chapter_id']
    ch_name = chapter['chapter_name']
    text    = chapter['text']

    RE_LE  = re.compile(r'^Bài \d+\.\s+.+$', re.MULTILINE)
    # RE_ECH = re.compile(r'^Bài tập cuối chương ', re.MULTILINE)
    RE_ECH = re.compile(r'^BÀI TẬP CUỐI CHƯƠNG [IVXLC0-9]+', re.MULTILINE)

    le_matches  = list(RE_LE.finditer(text))
    ech_match   = RE_ECH.search(text)

    intro = text[:le_matches[0].start()].strip() if le_matches else text.strip()
    intro = '\n'.join(intro.splitlines()[1:]).strip()

    lesson_list = '\n'.join(
        f"Bài {m.group().split('.')[0].split()[-1]}: {m.group().split('.', 1)[1].strip()}"
        for m in le_matches
    )

    # Lấy nội dung bài tập cuối chương
    ex_cuoi = text[ech_match.start():].strip() if ech_match else ''

    content = f"Chương {ch_id}: {ch_name}\n\n{intro}\n\nCác bài trong chương:\n{lesson_list}"
    if ex_cuoi:
        content += f"\n\n{ex_cuoi}"

    return {
        'type'   : 'chapter',
        'content': content,
        'metadata': {
            'type'        : 'chapter',
            'chapter_id'  : ch_id,
            'chapter_name': ch_name,
            'subject_type': CHAPTER_TYPE.get(ch_id, ''),
            'has_table': check_has_table(content),
        }
    }
def make_lesson_chunks(chapter: dict) -> list[dict]:
    ch_id   = chapter['chapter_id']
    ch_name = chapter['chapter_name']
    text    = chapter['text']

    RE_LE = re.compile(r'^Bài (\d+)\.\s+(.+)$', re.MULTILINE)
    matches = list(RE_LE.finditer(text))

    lessons = []
    for i, m in enumerate(matches):
        start = m.start()
        end   = matches[i+1].start() if i+1 < len(matches) else len(text)
        lessons.append({
            'lesson_id'  : m.group(1),
            'lesson_name': m.group(2).strip(),
            'text'       : text[start:end]
        })

    chunks = []
    RE_SEC = re.compile(r'^\d+\.\s+.+$', re.MULTILINE)
    RE_EX  = re.compile(r'^BÀI TẬP$', re.MULTILINE)

    for le in lessons:
        le_id   = le['lesson_id']
        le_name = le['lesson_name']
        le_text = le['text']

        # Intro = từ đầu đến mục 1 hoặc BÀI TẬP
        sec_matches = list(RE_SEC.finditer(le_text))
        ex_match    = RE_EX.search(le_text)

        intro_end = sec_matches[0].start() if sec_matches else (ex_match.start() if ex_match else len(le_text))
        intro = '\n'.join(le_text[:intro_end].strip().splitlines()[1:]).strip()

        # Danh sách mục
        section_list = '\n'.join(m.group().strip() for m in sec_matches)

        # Bài tập
        ex_text = le_text[ex_match.start():].strip() if ex_match else ''

        content = f"Chương {ch_id}: {ch_name} | Bài {le_id}: {le_name}\n\n{intro}"
        if section_list:
            content += f"\n\nCác mục trong bài:\n{section_list}"
        if ex_text:
            content += f"\n\n{ex_text}"

        chunks.append({
            'type'   : 'lesson',
            'content': content,
            'metadata': {
                'type'        : 'lesson',
                'chapter_id'  : ch_id,
                'chapter_name': ch_name,
                'lesson_id'   : le_id,
                'lesson_name' : le_name,
                'subject_type': CHAPTER_TYPE.get(ch_id, ''),
                'has_table': check_has_table(content),
            }
        })

    return chunks

def make_section_chunks(chapter: dict) -> list[dict]:
    ch_id   = chapter['chapter_id']
    ch_name = chapter['chapter_name']
    text    = chapter['text']

    RE_LE  = re.compile(r'^Bài (\d+)\.\s+(.+)$', re.MULTILINE)
    RE_SEC = re.compile(r'^(\d+)\.\s+(.+)$', re.MULTILINE)
    RE_EX  = re.compile(r'^BÀI TẬP$', re.MULTILINE)

    le_matches = list(RE_LE.finditer(text))
    chunks = []

    for i, le_m in enumerate(le_matches):
        le_id   = le_m.group(1)
        le_name = le_m.group(2).strip()

        le_start = le_m.start()
        le_end   = le_matches[i+1].start() if i+1 < len(le_matches) else len(text)
        le_text  = text[le_start:le_end]

        # Bỏ phần BÀI TẬP
        ex_match = RE_EX.search(le_text)
        main_text = le_text[:ex_match.start()] if ex_match else le_text

        sec_matches = list(RE_SEC.finditer(main_text))

        for j, sec_m in enumerate(sec_matches):
            sec_id   = sec_m.group(1)
            sec_name = sec_m.group(2).strip()

            sec_start = sec_m.start()
            sec_end   = sec_matches[j+1].start() if j+1 < len(sec_matches) else len(main_text)
            sec_text  = main_text[sec_start:sec_end].strip()

            content = (
                f"Chương {ch_id}: {ch_name} | "
                f"Bài {le_id}: {le_name} | "
                f"Chủ đề {sec_id}: {sec_name}\n\n"
                f"{sec_text}"
            )

            chunks.append({
                'type'   : 'section',
                'content': content,
                'metadata': {
                    'type'        : 'section',
                    'chapter_id'  : ch_id,
                    'chapter_name': ch_name,
                    'lesson_id'   : le_id,
                    'lesson_name' : le_name,
                    'section_id'  : sec_id,
                    'section_name': sec_name,
                    'subject_type': CHAPTER_TYPE.get(ch_id, ''),
                    'has_table': check_has_table(content),
                }
            })

    return chunks

def run(filepath):
    text     = Path(filepath).read_text(encoding='utf-8')
    chapters = split_chapters(text)

    all_chunks = []
    for ch in chapters:
        all_chunks.append(make_chapter_chunk(ch))
        all_chunks.extend(make_lesson_chunks(ch))
        all_chunks.extend(make_section_chunks(ch))

    print(f"Tổng chunks: {len(all_chunks)}")
    return all_chunks

if __name__ == '__main__':
    path = r'D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\rag\documents\toan_10\grade_10_chan_troi_sang_tao_toan_1.md'
    chapters = split_chapters(path)

    all_chunks = []
    for ch in chapters:
        all_chunks.append(make_chapter_chunk(ch))
        all_chunks.extend(make_lesson_chunks(ch))
        all_chunks.extend(make_section_chunks(ch))

    print(f"Tổng chunks: {len(all_chunks)}")

    for chunk in all_chunks:
        chunk['content'] = norm(chunk['content'])



    print("--------------\nChưa đưa vè unicode\n", all_chunks[6])

    print("--------------\nĐã đưa vè unicode\n",all_chunks[6]['content'], "\n-----\nmetadata",all_chunks[6]['metadata'])