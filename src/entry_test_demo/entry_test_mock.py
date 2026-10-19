"""Bài test giả lập Toán 10: không gọi LLM, tương thích entry_grade.py."""
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANK = HERE / 'question_bank_toan10.json'
CHAPTERS = ('I', 'II', 'III', 'IV', 'V', 'VI')


def create_mock_test(student_model: dict, count: int = 20, seed: int = 42, output_dir: Path | None = None) -> dict:
    if count <= 0:
        raise ValueError('count phải > 0')
    data = json.loads(BANK.read_text(encoding='utf-8'))
    subject = 'Toán 10'
    nl = next((x for x in student_model.get('nang_luc', []) if x.get('mon_hoc') == subject), None)
    if nl is None:
        raise ValueError('StudentModel chưa có nang_luc môn Toán 10')

    weak = set(nl.get('diem_yeu') or []) & set(CHAPTERS)
    strong = set(nl.get('diem_manh') or []) & set(CHAPTERS)
    known = weak | strong
    selected_chapters = [c for c in CHAPTERS if c in known] or list(CHAPTERS)
    if count < len(selected_chapters):
        raise ValueError('Số câu không đủ để đánh giá ít nhất 1 câu/chương')

    questions_by_ch = {ch: [x for x in data['questions'] if x['chapter_id'] == ch] for ch in selected_chapters}
    rng = random.Random(seed)
    # Ưu tiên tối thiểu 3 câu/chương nếu đủ; các câu còn lại ưu tiên chương yếu.
    minimum = min(3, count // len(selected_chapters))
    allocation = {ch: minimum for ch in selected_chapters}
    for _ in range(count-minimum*len(selected_chapters)):
        available = [ch for ch in selected_chapters if allocation[ch] < len(questions_by_ch[ch])]
        if not available:
            raise ValueError('Ngân hàng câu hỏi không đủ số lượng')
        chosen = rng.choices(available, weights=[3 if ch in weak else 1 for ch in available],k=1)[0]
        allocation[chosen] += 1

    picked=[]
    for ch in selected_chapters:
        picked += rng.sample(questions_by_ch[ch],allocation[ch])
    rng.shuffle(picked)
    # entry_grade.py đọc file key chứa questions với no, chapter_id, answer.
    answer_key=[]; public=[]
    for i,q in enumerate(picked,1):
        answer_key.append({'no':i,'chapter_id':q['chapter_id'],'answer':q['answer']})
        public.append({'no':i,'chapter_id':q['chapter_id'],'question':q['question'],'options':q['options']})

    outdir=Path(output_dir or HERE/'output')
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/'test_public.json').write_text(json.dumps({'subject':subject,'questions':public},ensure_ascii=False,indent=2),encoding='utf-8')
    key_file=outdir/'answer_key.json'
    key_file.write_text(json.dumps({'subject':subject,'questions':answer_key},ensure_ascii=False,indent=2),encoding='utf-8')
    lines=[]
    for q in public:
        lines.append(f"{q['no']}. [Chương {q['chapter_id']}] {q['question']}")
        lines += [f"   {letter}. {value}" for letter,value in q['options'].items()]
        lines.append('')
    (outdir/'test_student.txt').write_text('\n'.join(lines),encoding='utf-8')
    return {'subject':subject,'key_file':str(key_file.resolve()),'count':count,'allocation':allocation,'public_file':str((outdir/'test_public.json').resolve())}


def parse_answers(text: str) -> dict[int,str]:
    """Giống entry_grade.py: 1-A, 2 - C, 3b,..."""
    return {int(n):a.lower() for n,a in re.findall(r'(\d+)\s*[-–—:.)]*\s*([A-Da-d])(?![A-Za-z])',text or '')}


def grade_test(key_file: str, student_answers: str) -> dict:
    questions=json.loads(Path(key_file).read_text(encoding='utf-8'))['questions']
    ans=parse_answers(student_answers)
    by_ch={}; right=0
    for q in questions:
        stat=by_ch.setdefault(q['chapter_id'],{'total':0,'correct':0})
        stat['total']+=1
        if ans.get(q['no'])==q['answer'].lower():
            stat['correct']+=1;right+=1
    return {'total':len(questions),'correct':right,'answered':sum(q['no'] in ans for q in questions),'chapters':by_ch}


if __name__=='__main__':
    example={'nang_luc':[{'mon_hoc':'Toán 10','diem_yeu':['I','II'],'diem_manh':['III','IV']}]}
    info=create_mock_test(example)
    print('Đã tạo bài test:',info)
    print('\nĐỀ THI:\n')
    print((Path(info['key_file']).parent/'test_student.txt').read_text(encoding='utf-8'))
    answers=input('Nhập đáp án (ví dụ 1-A, 2-C, ...): ').strip()
    print('Kết quả:',json.dumps(grade_test(info['key_file'],answers),ensure_ascii=False,indent=2))
