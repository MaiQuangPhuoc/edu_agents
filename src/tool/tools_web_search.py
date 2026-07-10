# # import requests
# # from langchain.tools import tool
# # from duckduckgo_search import DDGS
# # from bs4 import BeautifulSoup
# # import os







# # tools.py
# from langchain_community.tools import DuckDuckGoSearchResults

# def get_tools():
#     """
#     Trả về danh sách các tool cho agent.
#     Ở đây chỉ dùng DuckDuckGo để search internet.
#     """
#     return [
#         DuckDuckGoSearchResults(
#             name="internet_search"
#         )
#     ]

















# # from dotenv import load_dotenv
# # from langchain_community.tools.tavily_search import TavilySearchResults
# # load_dotenv()

# # # TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

# # @tool("internet_search_DDGO", return_direct=False)
# # def internet_search_DDGO(query: str) -> str:

# #   """Searches the internet using DuckDuckGo."""

# #   with DDGS() as ddgs:
# #     results = [r for r in ddgs.text(query, max_results=5)]
# #     # return results if results else "No results found."
# #     return str(results) if results else "No results found."

# # @tool("process_content", return_direct=False)
# # def process_content(url: str) -> str:

# #     """Processes content from a webpage."""

# #     # response = requests.get(url)
# #     response = requests.get(url, headers={'User-Agent': '...'}, timeout=10)
# #     soup = BeautifulSoup(response.content, 'html.parser')
# #     return soup.get_text()

# # # @tool("internet_search", return_direct=False)
# # # def internet_search(query: str) -> str:
# # #     """Searches the internet using Tavily."""
# # #     search_tool = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=5)
# # #     results = search_tool.invoke(query)

# # #     # Log the raw results for debugging purposes
# # #     print("Raw results:", results)

# # #     if isinstance(results, list) and all(isinstance(result, dict) for result in results):
# # #         formatted_results = ""
# # #         references = []
# # #         for i, result in enumerate(results):
# # #             title = result.get('title', 'No Title')
# # #             url = result.get('url', 'No URL')
# # #             snippet = result.get('snippet', 'No Snippet')
# # #             formatted_results += f"{i+1}. {title}\n{snippet} [^{i+1}]\n\n"
# # #             references.append(f"[^{i+1}]: [{title}]({url})")

# # #         references_section = "\n**References:**\n" + "\n".join(references)
# # #         return formatted_results + references_section

# # #     else:
# # #         return "Unexpected result format. Please check the Tavily API response structure."

# # def get_tools():
# #     # return [internet_search]   
# #     return [internet_search_DDGO, process_content]   


from tavily import TavilyClient
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.configs import env_config
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document



# u = env_config.api
# tavily_client = TavilyClient(api_key=env_config.api_key_tavily)



# query = "Mệnh đề, mệnh đề chứa biến là gì?"
# query = "Phương trình đường tròn có các tính chất nào, có các dạng bài tập nào?"
 


# print(api_key)

# response = tavily_client.search("Mệnh đề là gì?")
# response = tavily_client.extract("https://mira.vn/tieu-su-ve-lionel-messi")
# response = tavily_client.crawl("https://vietjack.com/toan-10-kn/ly-thuyet-bai-1-menh-de.jsp", instructions="Mệnh đề, mệnh đề chứa biến là gì?")


# response = tavily_client.get_search_context(query="Mệnh đề, mệnh đề chứa biến là gì?")
# response = tavily_client.qna_search(query="Mệnh đề, mệnh đề chứa biến là gì?")

# urls = "https://loigiaihay.com/ly-thuyet-ve-menh-de-c45a4751.html" 


# search_tool = TavilySearchResults(api_key=env_config.api_key_tavily, max_results=5)


# Log the raw results for debugging purposes
# print("Raw results:", results)


# query="tập hợp là gì, tập hợp và mệnh đề liên quan như thế nào?"

# os.environ["TAVILY_API_KEY"] = env_config.api_key_tavily

# search_tool = TavilySearchResults(max_results=5)
# response = search_tool.invoke(query)

# print("---"*30)

# for i, item in enumerate(response, 1):
#     content = item.get("content", "")
#     score = item.get("score", None)
#     url = item.get("url", "")

#     print(f"👉 --------------[ {i} ]-------------- Score: {score:.4f}-----------------\n👉 {url}\n")
#     print("✅ ",content, "...\n")

def tools_web_search(query: str, api_key: str, max_results: int = 5):
    """
    Tìm kiếm trên internet bằng TavilySearchResults.
    Trả về danh sách dict chứa content, url, score.
    """
    os.environ["TAVILY_API_KEY"] = api_key
    search_tool = TavilySearchResults(max_results=max_results)

    response = search_tool.invoke(query)

    results = []
    for item in response:
        score = item.get("score", 0.0)
        if score >= 0.5:
            # results.append({
            #     "page_content": item.get("content", ""),
            #     "url": item.get("url", ""),
            #     "score": item.get("score", 0.0)
            # })
            results.append(
                Document(
                    page_content=item.get("content", ""),
                    metadata={
                        "url": item.get("url", ""),
                        "score": score
                    }
                )
            )
    return results