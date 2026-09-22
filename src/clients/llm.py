


import json
import logging, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from typing import List, Optional, Union
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import BaseTool
from pydantic import BaseModel
import time, re
from src.configs import env_config

logger = logging.getLogger(__name__)

def _extract_failed(e) -> str:
        body = getattr(e, "body", None)
        if isinstance(body, dict):
            return body.get("failed_generation") or (body.get("error") or {}).get("failed_generation") or ""
        return ""

def _recover_from_failed(failed: str, output_model):
        if not failed:
            return None
        m = re.search(r'\{.*\}', failed, re.DOTALL)
        if not m:
            return None
        raw = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', m.group())
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and "arguments" in data:
                data = data["arguments"]
            return output_model.model_validate(data)
        except Exception:
            return None

class LLMClient:
    """LLM client hỗ trợ groq / openai / openrouter, bật/tắt bằng cách
    đổi api_provider trong .env, không cần sửa code."""

    def __init__(self, model: str, api_provider: str = None):
        self.model = model
        self.api_provider = api_provider or env_config.api_provider
        self._llm = self._initialize_llm()





    
    def _initialize_llm(self):
        provider = self.api_provider

        if provider == "groq":
            from langchain_groq import ChatGroq
            if not env_config.groq_api_key:
                raise ValueError("Thiếu GROQ_API_KEY trong .env")
            return ChatGroq(model=self.model, groq_api_key=env_config.groq_api_key)

        elif provider == "openai":
            from langchain_openai import ChatOpenAI
            if not env_config.openai_api_key:
                raise ValueError("Thiếu OPENAI_API_KEY trong .env")
            return ChatOpenAI(model=self.model, api_key=env_config.openai_api_key)

        elif provider == "openrouter":
            from langchain_openai import ChatOpenAI
            if not env_config.openrouter_api_key:
                raise ValueError("Thiếu OPENROUTER_API_KEY trong .env")
            return ChatOpenAI(
                model=self.model,
                api_key=env_config.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
            )

        else:
            raise ValueError(f"api_provider không hỗ trợ: {provider}")

    def _configure_llm(self, max_tokens, temperature, llm_tools, output_model):
        llm = self._llm.bind(max_tokens=max_tokens, temperature=temperature)
        if llm_tools:
            llm = llm.bind_tools(llm_tools)
        if output_model:
            llm = llm.with_structured_output(output_model)
        return llm

    def invoke_with_retries(self, prompt: ChatPromptTemplate, max_tokens=4096,
                             temperature=1, llm_tools: List[BaseTool] = None,
                             output_model: Optional[BaseModel] = None, num_retries=1):
        llm_tools = llm_tools or []
        llm = self._configure_llm(max_tokens, temperature, llm_tools, output_model)
        for attempt in range(num_retries):
            try:
                chain = prompt | llm
                response = chain.invoke(input={})
                logger.info(f"LLM invocation successful on attempt {attempt + 1}")
                return response
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == num_retries - 1:
                    raise
                logger.info(f"Retrying... {attempt + 2}/{num_retries}")

    async def ainvoke_with_retries(self, prompt: Union[ChatPromptTemplate, List[BaseMessage]],
                                    max_tokens=4096, temperature=1,
                                    llm_tools: List[BaseTool] = None,
                                    output_model: Optional[BaseModel] = None, num_retries=1):
        llm_tools = llm_tools or []
        llm = self._configure_llm(max_tokens, temperature, llm_tools, output_model)
        for attempt in range(num_retries):
            try:
                if isinstance(prompt, list):
                    return await llm.ainvoke(prompt)
                chain = prompt | llm
                return await chain.ainvoke(input={})
            except Exception as e:
                logger.error(f"Lỗi ở lần thử thứ {attempt + 1}: {e}")
                if attempt == num_retries - 1:
                    raise
                logger.info(f"Đang thử lại... ({attempt + 2}/{num_retries})")

    # def invoke_structured(self, output_model: BaseModel, messages: list,
    #                        max_retries: int = 3, max_tokens: int = 4096, fallback=None):
    #     """Giống hệt cách dùng cũ (_llm.with_structured_output(...).invoke(...)),
    #     chỉ thêm max_tokens và chờ (backoff) khi retry."""
    #     structured_llm = self._llm.bind(max_tokens=max_tokens).with_structured_output(output_model)

    #     for attempt in range(max_retries):
    #         try:
    #             result = structured_llm.invoke(messages)
    #             return result
    #         except Exception as e:
    #             err_str = str(e)
    #             print(f"[invoke_structured] {output_model.__name__} attempt {attempt + 1} lỗi: {e}")

    #             if "invalid_api_key" in err_str.lower() or "expired_api_key" in err_str.lower():
    #                 raise

    #             if attempt < max_retries - 1:
    #                 m = re.search(r'try again in ([\d.]+)s', err_str)
    #                 wait = float(m.group(1)) + 1 if m else 2
    #                 print(f"[invoke_structured] chờ {wait:.1f}s trước khi retry")
    #                 time.sleep(wait)

    #     return fallback




    def invoke_structured(self, output_model, messages: list,
                        max_retries: int = 3, max_tokens: int = 4096, fallback=None):
        base = self._llm.bind(max_tokens=max_tokens)
        tool_llm = base.with_structured_output(output_model)
        json_llm = base.with_structured_output(output_model, method="json_mode")
        json_messages = messages + [{
            "role": "user",
            "content": "Trả về DUY NHẤT một JSON object đúng schema sau, không markdown:\n"
                    + json.dumps(output_model.model_json_schema(), ensure_ascii=False),
        }]

        for attempt in range(max_retries):
            use_json_mode = attempt >= 1          # lần 1: tool calling, lần 2+: json_mode
            llm  = json_llm if use_json_mode else tool_llm
            msgs = json_messages if use_json_mode else messages
            try:
                return llm.invoke(msgs)
            except Exception as e:
                err_str = str(e)
                print(f"[invoke_structured] {output_model.__name__} attempt {attempt + 1} lỗi: {err_str[:200]}")

                if "invalid_api_key" in err_str.lower() or "expired_api_key" in err_str.lower():
                    raise

                recovered = _recover_from_failed(_extract_failed(e), output_model)
                if recovered is not None:
                    print("[invoke_structured] đã vớt được từ failed_generation")
                    return recovered

                if attempt < max_retries - 1:
                    m = re.search(r'try again in ([\d.]+)s', err_str)
                    time.sleep(float(m.group(1)) + 1 if m else 1)

        return fallback
    
# Global client — comment dòng dưới nếu không muốn auto-init lúc import
try:
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
except Exception as e:
    logger.error(f"Failed to initialize global LLM client: {e}")
    llm_client = None


# from langchain_core.messages import HumanMessage

# try:
#     llm_client = LLMClient(
#         model=env_config.model,
#         api_provider=env_config.api_provider
#     )
#     print("LLM phản hồi:")
#     # Dùng trực tiếp llm bên trong LLMClient để test
#     response = llm_client._llm.invoke([


#         HumanMessage(content="Hà Nội là thủ đô của Việt Nam là mệnh đề đúng hay sai")
#     ])


#     print(response.content)

# except Exception as e:
#     logger.error(f" Lỗi khởi tạo LLM client hoặc gọi LLM: {e}")