from loaders import DocumentLoader
from processors import DocumentProcessor
import re
from langchain_core.documents import Document
from vectorstores import VectorStoreManager
from retrievers import VectorStoreRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

import sys , os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".." ,"..")))
from src.clients.embedding import embeddings_qa
from src.configs import env_config
# from src.clients.databases import qdrant_qa


# from langchain.embeddings import HuggingFaceBgeEmbeddings

# 1 loader 

file_path = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\rag\documents\toan_10\grade_10_canh_dieu_toan_1.md"


loader = DocumentLoader(file_path)

docs = loader.load()


# print(docs)
if docs:
    print("Đã load thành công file")
else:
    print("Load thất bại hoặc file trống")



# 2 chunking (nối metadata vào page_content)

raw_text = "\n".join(doc.page_content for doc in docs)

chapter_blocks = re.split(r"(?=CHƯƠNG\s+[IVXLCDM\d]+[:]?.*)", raw_text)

# In thử demo 200 ký tự đầu tiên của mỗi block
# for i, block in enumerate(chapter_blocks):
#     if block.strip():  # bỏ block rỗng
#         print(f"--- Block {i} ---")
#         print(block[:200].replace("\n", " "))
#         print()

# print(chapter_blocks[1])

def extract_chapter_title(text: str) -> str:
    # lấy dòng đầu tiên
    first_line = text.strip().split("\n")[0]
    return first_line

documents = []

for i in range(1, len(chapter_blocks), 1):  # mỗi phần tử = 1 chương
    chapter_raw = chapter_blocks[i].strip()
    if not chapter_raw:
        continue
    
    # --- lấy tiêu đề chương ---
    chapter_title = extract_chapter_title(chapter_raw)
    
    # --- tách các bài trong chương ---
    lesson_blocks = re.split(r"(?=Bài\s+\d+\.?.*)", chapter_raw)
    for block in lesson_blocks:
        block = block.strip()
        if not block or not block.startswith("Bài"):
            continue
        
        # lấy tiêu đề bài (dòng đầu tiên)
        lesson_title = block.split("\n")[0].strip()
        lesson_content = "\n".join(block.split("\n")[1:]).strip()
        # new_page_content = f"{chapter_title} - {lesson_title}\n{lesson_content}"
        
        # tạo Document
        doc = Document(
            page_content=lesson_content,
            metadata={
                "CHƯƠNG": chapter_title,
                "BÀI": lesson_title
            }
        )
        documents.append(doc)

# kiểm tra
# for i, doc in enumerate(documents):
#     print(f"--- Doc {i} ---")
#     print(f"metadata: {doc.metadata}\n----------")
#     print(f"doc.page_content: {doc.page_content[:200]}\n----------")

# print("doc_0: ", documents[0])



text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1300,     # characters
    chunk_overlap=150,
    separators=["\n\n","\n",".", "!", "?", " ", ""]
)

chunks = []
for doc in documents:
    splits = text_splitter.split_text(doc.page_content)
    for split in splits:
        chunks.append(Document(
            page_content=split,
            metadata=doc.metadata
        ))
 
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    chapter = chunk.metadata.get("CHƯƠNG","")
    lesson = chunk.metadata.get("BÀI" , "")
    chunk.page_content = f"{chapter} - {lesson}\n{chunk.page_content}"
    # print(chunk.page_content[:200])
    # print("------\nMetadata:", chunk.metadata)
    # print("-" * 100)
print("-" * 100)
print("-" * 100)
print(chunks[12])
print("-" * 100)
print(chunks[13])
print("-" * 100)
print(chunks[14])


# ----------------------------------------



# 3 embedding + lưu trên cloud của Qdrant 

vector_manager = VectorStoreManager(
    url = env_config.qdrant_url,
    api_key=env_config.qdrant_api_key
)


collection_name = "toan_10"
vector_store = vector_manager.create_vector_store(
    documents=chunks,
    embeddings=embeddings_qa,  # <-- truyền object model, KHÔNG encode trước
    collection_name=collection_name
)




# ----------------------------temp-------------------

# client = vector_manager.get_client()

# collection_info = client.get_collection(collection_name="toan10_chunks")
# print("Collection info:", collection_info)

# # Hoặc in số lượng vector đã lưu
# points_count = collection_info.vectors_count
# print(f"Số vector đã lưu: {points_count}")


# query = "hàm số bậc hai"

# retrieved_docs = vector_store.similarity_search(query, k=3)
# for i, doc in enumerate(retrieved_docs, 1):
#     print(f"\nKết quả {i}:")
#     print(doc.page_content[:300])  # In 300 ký tự đầu tiên

#### end temp

# 4. retreiver 

#4.1 retriever with similarity 
# retriever = VectorStoreRetriever(vector_store=qdrant_qa, search_kwargs={"k": 3})

# query = "mệnh đề là gì"
# results = retriever.retrieve(query)
# for i, result in enumerate(results ,1):
#     print(f"\n----documents : {i}-----")
#     print(result.page_content)
#     print("metadata : {result.metadata}")


# 4.2 retriever with as_retriever 

# my_retriever = VectorStoreRetriever(vector_store=qdrant)
# base_retriever  = my_retriever.as_retriever()

# query = "mệnh đề và hàm số bậc hai"
# docs = base_retriever.invoke(query)

# for i,doc in enumerate(docs , 1):
#     print(f"\n----- Documents :{i}-----")
#     print(doc.page_content)
#     print("-" * 40 )


# ----------------------------temp-------------------
