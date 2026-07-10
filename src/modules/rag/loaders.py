# import logging

# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     CSVLoader,
#     WebBaseLoader,
#     Docx2txtLoader,
#     UnstructuredLoader,
#     UnstructuredMarkdownLoader
# )
# # from langchain_unstructured import UnstructuredLoader

# logger = logging.getLogger(__name__)


    
# class DocumentLoader:
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         logger.info(f"DocumentLoader initialized with file: {self.file_path}")

#     def get_loader(self, file_path: str):
#         if file_path.endswith(".pdf"):
#             return PyPDFLoader(file_path)
#         elif file_path.endswith(".csv"):
#             return CSVLoader(file_path)
#         elif file_path.endswith(".docx"):
#             return Docx2txtLoader(file_path)  # ✅ Sử dụng đúng loader cho docx
#         elif file_path.endswith(".md") or file_path.endswith(".markdown"):
#             return UnstructuredMarkdownLoader(file_path)
#         elif file_path.startswith("http"):
#             return WebBaseLoader(file_path)
#         else:
#             return UnstructuredLoader(file_path)
#     def load(self):
#         loader = self.get_loader(self.file_path)
#         docs = loader.load()

#         if docs:
#             print('đã load file thành công ')
#         else:
#             print('Chưa lòad được file ??? ')
        
#         logger.info(f"Loading document from {self.file_path}")
#         return docs

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
    WebBaseLoader,
    UnstructuredFileLoader,
    UnstructuredMarkdownLoader
)

class DocumentLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_loader(self, file_path: str):
        if file_path.endswith(".pdf"):
            return PyPDFLoader(file_path)
        elif file_path.endswith(".csv"):
            return CSVLoader(file_path)
        elif file_path.endswith(".docx"):
            return Docx2txtLoader(file_path)
        elif file_path.endswith(".md") or file_path.endswith(".markdown"):
            return UnstructuredMarkdownLoader(file_path)
        elif file_path.startswith("http"):
            return WebBaseLoader(file_path)
        else:
            return UnstructuredFileLoader(file_path)

    def load(self):
        loader = self.get_loader(self.file_path)
        docs = loader.load()

        if docs:
            print("Đã load file thành công")
        else:
            print("Chưa load được file ???")

        return docs
