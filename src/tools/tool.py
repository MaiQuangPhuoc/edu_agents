from langchain_core.tools import tool 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state import AgentProfile  , DailyInfo , FeedbackResult, get_id_plan

from src.clients.databases import qdrant
from src.modules.rag.retrievers import VectorStoreRetriever
from src.configs import env_config

# def create_retrieve_tool(vector_db, retrieve_count: int):
#     """Create retrieve tool for the bot."""
#     @tool(response_format="content")
#     def retrieve(query: str):
#         """Retrieve information related to a query."""
#         retrieved_docs = vector_db.db.similarity_search(
#             query, 
#             k=retrieve_count,
#         )
#         content = "\n\n".join(
#             f"Content: {doc.page_content}"
#             for doc in retrieved_docs
#         )
#         return content
#     return retrieve

# def retrieve_tool(vector_store, search_kwargs):
#     """crearte retrieve tool """
#     @tool(response_format="content")
#     def retrieve(query: str):
#         """retriever documents"""
#         my_retriever = VectorStoreRetriever(
#             vector_store=vector_store,
#             search_kwargs=search_kwargs
#         )
#         base_retriever = my_retriever.as_retriever()
#         docs = base_retriever.invoke(query)
#         return docs
#     return retrieve


def retrieve_tool(vector_store, search_kwargs):
    """Tạo retriever tool dùng lại nhiều lần."""
    my_retriever = VectorStoreRetriever(
        vector_store=vector_store,
        search_kwargs=search_kwargs
    )
    # base_retriever = my_retriever.as_retriever()
    # base_retriever = my_retriever.retrieve()


    @tool(response_format="content")
    def retrieve(query: str):
        """Truy vấn tài liệu từ vector store."""
        return my_retriever.retrieve(query)

    return retrieve

def retrieve_tool_score(vector_store, search_kwargs):
    """Tạo retriever tool dùng lại nhiều lần."""
    my_retriever = VectorStoreRetriever(
        vector_store=vector_store,
        search_kwargs=search_kwargs
    )

    @tool(response_format="content")
    def retrieve_score(query: str):
        """Truy vấn tài liệu từ vector store."""
        return my_retriever.retrieve_score(query)

    return retrieve_score


def get_id_tools(llm_client, state :get_id_plan):
    """Create tool for parsing output.""" 
    @tool(response_format="content_and_artifact")
    def parse_id(query: str):
        """Tool để trích xuất id từ input để lấy đúng file.json ."""
        
        llm_output = llm_client._llm.with_structured_output(state)
        
        response = llm_output.invoke(query)
        
        return "Đang xử id của bạn..." if response else "Không thể trích xuất id .", response
    
    return parse_id



def create_parser_output_tool(llm_client, state :AgentProfile):
    """Create tool for parsing output.""" 
    @tool(response_format="content_and_artifact")
    def parse_outputt(query: str):
        """Tool để trích xuất hồ sơ học tập từ người học."""
        
        llm_output = llm_client._llm.with_structured_output(state)
        
        response = llm_output.invoke(query)
        
        return "Đang xử lý hồ sơ học tập của bạn..." if response else "Không thể trích xuất hồ sơ học tập.", response
    
    return parse_outputt

def create_daily_tool(llm_client, state :DailyInfo):
    """Create tool for parsing output.""" 
    @tool(response_format="content_and_artifact")
    def parse_outputt(query: str):
        """Tool để trích xuất hồ sơ học tập từ người học."""
        
        llm_output = llm_client._llm.with_structured_output(state)
        
        response = llm_output.invoke(query)
        
        return "Đang xử lý hồ sơ học tập của bạn..." if response else "Không thể trích xuất hồ sơ học tập.", response
    
    return parse_outputt


# def review_tools(llm_client, state: FeedbackResult):
#     """Create tool for review tools parsing output."""
#     @tool(response_format="content_and_artifact") 
#     def tool_review(query: str):
#         """Tool để trích xuất các phản hổi hài lòng hay không hài lòng về kế hoạch học từ người học."""
        
#         llm_output = llm_client.with_structured_output(state)
#         response = llm_output.invoke(query)
#         return "Đang xử lý phản hồi của bạn..." if response else "Không thể trích xuất phản hồi của bạn.", response

#     return tool_review


def review_tools(llm_client, state: FeedbackResult):
    """Create tool for review tools parsing output."""
    @tool(response_format="content_and_artifact") 
    def tool_review(query: str):
        """Tool để trích xuất các phản hồi hợp lệ về kế hoạch học từ người học,
        kết quả luôn trả về JSON theo schema FeedbackResult."""
        llm_output = llm_client._llm.with_structured_output(state)
        response = llm_output.invoke(query)
        return (
            "Đang xử lý phản hồi..." if response else "Không thể trích xuất phản hồi",
            response
        )
    return tool_review




