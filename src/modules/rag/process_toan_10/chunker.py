import re
from pathlib import Path
import json
import sys , os 
import copy
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..","..")))
# from src.modules.rag.vectorstores2 import VectorStoreManager

from langchain_core.documents import Document
from src.clients.embedding import embeddings_qa
# from src.configs import env_config


# from langchain_core.documents import Document
# from docx import Document
# from langchain.schema import Document


print(" =============================== chunker =============================== ")

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


# đếm từ 
def count_words(doc):
    return len(doc.page_content.split())


# đếm token từ model embedding trả vè 
def count_tokens_chunks(documents, embeddings_qa):

    tokenizer = embeddings_qa._client.tokenizer
    max_len = embeddings_qa._client.max_seq_length

    num_ok = 0
    num_small = 0
    num_over = 0

    print(f"{'Chunk':<10} | {'Token':<6} | Trạng thái")
    print("-" * 60)

    for i, doc in enumerate(documents, start=1):

        n_tokens = len(
            tokenizer.encode(
                doc.page_content,
                add_special_tokens=True
            )
        )

        if n_tokens > max_len:
            note = "❌ VƯỢT NGƯỠNG"
            num_over += 1

        elif n_tokens < 100:
            note = "❌ CHƯA ĐẠT"
            num_small += 1

        else:
            note = "✅ ĐẠT"
            num_ok += 1

        print(
            f"chunk {i:<4} | {n_tokens:<6} | {note}"
        )

    print("-" * 60)
    print(f"✅ Đạt         : {num_ok}")
    print(f"❌ Chưa đạt    : {num_small}")
    print(f"❌ Vượt ngưỡng : {num_over}")
    print(f"📏 max_seq_length model: {max_len}")


# update metadata of chunk 
def normalize_math_metadata(all_chunks):

    for chunk in all_chunks:

        metadata = chunk["metadata"]

        chunk["metadata"] = {

            "type": " ",

            "subject": "Toán 10",

            "chapter_id":
                metadata.get("chapter_id", " "),

            "chapter_name":
                metadata.get("chapter_name", " "),

            "lesson":
                metadata.get("lesson_name", " "),

            "id_lesson":
                metadata.get("lesson_id", " "),

            "section_id":
                metadata.get("section_id", " "),

            "section_name":
                metadata.get("section_name", " "),

            "sub_id":
                metadata.get("sub_id", " "),

            "sub_name":
                metadata.get("sub_name", " "),

            "has_table":
                metadata.get("has_table", False),

            "sub_type":
                metadata.get("type", " ")
        }

    return all_chunks

# tách đoạn 
def count_tokens(text, embeddings_qa):
    tokenizer = embeddings_qa._client.tokenizer

    return len(
        tokenizer.encode(
            text,
            add_special_tokens=False
        )
    )


def split_by_paragraphs(
    content,
    embeddings_qa,
    max_tokens=250,
    min_tokens=50
):

    paragraphs = [
        p.strip()
        for p in content.split("\n\n")
        if p.strip()
    ]

    # =====================================
    # Bước 1:
    # xử lý paragraph quá dài
    # =====================================

    normalized_paragraphs = []

    for para in paragraphs:

        para_tokens = count_tokens(
            para,
            embeddings_qa
        )

        if para_tokens <= max_tokens:

            normalized_paragraphs.append(para)

        else:

            # tách theo câu

            sentences = re.split(
                r'(?<=[.!?])\s+',
                para
            )

            current = []
            current_tokens = 0

            for sent in sentences:

                sent_tokens = count_tokens(
                    sent,
                    embeddings_qa
                )

                if current_tokens + sent_tokens <= max_tokens:

                    current.append(sent)
                    current_tokens += sent_tokens

                else:

                    if current:
                        normalized_paragraphs.append(
                            " ".join(current)
                        )

                    current = [sent]
                    current_tokens = sent_tokens

            if current:

                normalized_paragraphs.append(
                    " ".join(current)
                )

    # =====================================
    # Bước 2:
    # ghép paragraph thành chunk
    # =====================================

    chunks = []

    current = []
    current_tokens = 0

    for para in normalized_paragraphs:

        para_tokens = count_tokens(
            para,
            embeddings_qa
        )

        if current_tokens + para_tokens <= max_tokens:

            current.append(para)
            current_tokens += para_tokens

        else:

            if current:

                chunks.append(
                    "\n\n".join(current)
                )

            current = [para]
            current_tokens = para_tokens

    if current:

        chunks.append(
            "\n\n".join(current)
        )

    # =====================================
    # Bước 3:
    # merge chunk quá nhỏ
    # =====================================

    merged_chunks = []

    for chunk in chunks:

        if not merged_chunks:

            merged_chunks.append(chunk)
            continue

        chunk_tokens = count_tokens(
            chunk,
            embeddings_qa
        )

        prev_tokens = count_tokens(
            merged_chunks[-1],
            embeddings_qa
        )

        if (
            chunk_tokens < min_tokens
            and prev_tokens + chunk_tokens <= max_tokens
        ):

            merged_chunks[-1] += "\n\n" + chunk

        else:

            merged_chunks.append(chunk)

    return merged_chunks


# chunk theo 3 trường hợp 
def split_math_chunks(
    all_chunks,
    embeddings_qa,
    max_tokens=250
):
    """
    Xử lý chunk Toán:
    - chapter:
        Nội dung + BÀI TẬP CUỐI CHƯƠNG
    - lesson:
        Nội dung + BÀI TẬP
    - section:
        Chỉ nội dung

    Sau đó chunk lại theo đoạn và giới hạn token.
    """

    new_chunks = []

    def add_chunks(content, metadata, chunk_type):
        """
        Helper tạo sub-chunks và cập nhật type.
        """

        if not content.strip():
            return

        chunks = split_by_paragraphs(
            content=content,
            embeddings_qa=embeddings_qa,
            max_tokens=max_tokens
        )

        for c in chunks:

            meta = copy.deepcopy(metadata)
            meta["type"] = chunk_type

            new_chunks.append({
                "metadata": meta,
                "content": c.strip()
            })

    for chunk in all_chunks:

        metadata = chunk["metadata"]
        content = chunk["content"]

        sub_type = metadata.get("sub_type", "")

        # ==================================================
        # CHAPTER
        # ==================================================
        if sub_type == "chapter":

            parts = re.split(
                r'BÀI\s+TẬP\s+CUỐI\s+CHƯƠNG\s+[IVXLCDM]+',
                content,
                maxsplit=1
            )

            if len(parts) == 2:

                noi_dung = parts[0]
                cau_hoi = parts[1]

                add_chunks(
                    noi_dung,
                    metadata,
                    "noi_dung"
                )

                add_chunks(
                    cau_hoi,
                    metadata,
                    "cau_hoi"
                )

            else:

                add_chunks(
                    content,
                    metadata,
                    "noi_dung"
                )

        # ==================================================
        # LESSON
        # ==================================================
        elif sub_type == "lesson":

            parts = re.split(
                r'\bBÀI\s+TẬP\b',
                content,
                maxsplit=1
            )

            if len(parts) == 2:

                noi_dung = parts[0]
                cau_hoi = parts[1]

                add_chunks(
                    noi_dung,
                    metadata,
                    "noi_dung"
                )

                add_chunks(
                    cau_hoi,
                    metadata,
                    "cau_hoi"
                )

            else:

                add_chunks(
                    content,
                    metadata,
                    "noi_dung"
                )

        # ==================================================
        # SECTION
        # ==================================================
        elif sub_type == "section":

            add_chunks(
                content,
                metadata,
                "noi_dung"
            )

        # ==================================================
        # KHÁC
        # ==================================================
        else:

            add_chunks(
                content,
                metadata,
                "noi_dung"
            )

    return new_chunks

# save all chunk markdown 
def save_chunks_to_markdown(
    all_chunks,
    output_path,
    embeddings_qa
):

    tokenizer = embeddings_qa._client.tokenizer
    max_len = embeddings_qa._client.max_seq_length

    with open(output_path, "w", encoding="utf-8") as f:

        for idx, chunk in enumerate(all_chunks, start=1):

            n_tokens = len(
                tokenizer.encode(
                    chunk["content"],
                    add_special_tokens=True
                )
            )

            if n_tokens > max_len:
                status = "❌❌❌ VƯỢT NGƯỠNG"

            elif n_tokens < 100:
                status = "❌❌❌ CHƯA ĐẠT"

            else:
                status = "✅ ĐẠT"

            f.write(
                f"<!-- chunk {idx} ---- {status} ----- {n_tokens} token -->\n"
            )

            f.write("---\n")

            for key, value in chunk["metadata"].items():
                f.write(f"{key}: {value}\n")

            f.write("---\n")

            f.write(chunk["content"].strip())
            f.write("\n\n\n")

    print(f"✓ Đã lưu {len(all_chunks)} chunks")
    print(f"✓ File: {output_path}")

if __name__ == '__main__':

    path_origin = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents"

    path = path_origin + r"\grade_10_chan_troi_sang_tao_toan_1.md"

    # path = r'D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\grade_10_chan_troi_sang_tao_toan_1.md'
    chapters = split_chapters(path)

    all_chunks = []
    for ch in chapters:
        all_chunks.append(make_chapter_chunk(ch))
        all_chunks.extend(make_lesson_chunks(ch))
        all_chunks.extend(make_section_chunks(ch))

    all_chunks = normalize_math_metadata(all_chunks)

    all_chunks = split_math_chunks(
        all_chunks=all_chunks,
        embeddings_qa=embeddings_qa,
        max_tokens=250
    )

    for chunk in all_chunks:
        chunk['content'] = norm(chunk['content'])

    documents = [
        Document(page_content=chunk['content'], metadata=chunk['metadata'])
        for chunk in all_chunks
    ]

    count_tokens_chunks(documents, embeddings_qa)

    # for i, doc in enumerate(documents[:10], 1):
    #     print(f"\n---------------------------\nChunk {i}: {count_words(doc)} từ\n")


    # for i, doc in enumerate(documents[:4], start=1):
    #     print(f"Document {i}")
    #     print(doc)
    #     print("-" * 100)

    # for i, doc in enumerate(documents[218:223], start=1):

    #     print(f"\nDocument {i}")

    #     print("\nMETADATA")
    #     print("-" * 40)
    #     print(doc.metadata)

    #     # print("\nCONTENT")
    #     # print("-" * 40)
    #     # print(doc.page_content)

    #     print("\n" + "=" * 100)


    lengths = []

    for doc in documents:
        lengths.append(
            len(
                embeddings_qa._client.tokenizer.encode(
                    doc.page_content,
                    add_special_tokens=True
                )
            )
        )

    print(f"Min: {min(lengths)}")
    print(f"Max: {max(lengths)}")
    print(f"Avg: {sum(lengths)/len(lengths):.1f}")


    # gọi hàm save chunk 
    save_chunks_to_markdown(
        all_chunks,
        r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\toan\toan_10_chunk_final_ver1_1.md",
        embeddings_qa
    )

    # print("-"*40)
    # vector_manager = VectorStoreManager(
    #     url = env_config.qdrant_url,
    #     api_key=env_config.qdrant_api_key
    # )


    # # vector_store = vector_manager.create_vector_store(
    # #     documents=documents,
    # #     embeddings=embeddings_qa,
    # #     collection_name="doc_toan_10_1"    
    # # )
    

    # # print("Vector store created successfully with the provided documents and embeddings.")

    # import time

    # BATCH_SIZE = 10
    # batches = [documents[i:i+BATCH_SIZE] for i in range(0, len(documents), BATCH_SIZE)]

    # for i, batch in enumerate(batches):
    #     for attempt in range(3):  # retry 3 lần
    #         try:
    #             vector_store = vector_manager.create_vector_store(
    #                 documents=batch,
    #                 embeddings=embeddings_qa,
    #                 collection_name="documents"
    #             )
    #             print(f"✓ Batch {i+1}/{len(batches)}")
    #             time.sleep(1)  # nghỉ 1s giữa các batch
    #             break
    #         except Exception as e:
    #             print(f"Batch {i+1} lần {attempt+1} lỗi: {e}")
    #             time.sleep(3)

    # print(f"✓ Upload xong {len(documents)} chunks")