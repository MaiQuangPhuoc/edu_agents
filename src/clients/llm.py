


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

from pydantic import BaseModel, ValidationError


def _extract_failed(e) -> str:
    body = getattr(e, "body", None)
    if isinstance(body, dict):
        return body.get("failed_generation") or (body.get("error") or {}).get("failed_generation") or ""
    return ""


def _extract_json_block(text: str) -> dict | None:
    """Tìm khối JSON trong text tự do (kể cả lẫn markdown/giải thích), sửa backslash lỗi, parse."""
    if not text:
        return None
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if not m:
        return None
    raw = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', m.group())
    try:
        data = json.loads(raw)
    except Exception:
        return None
    if isinstance(data, dict) and "arguments" in data and "name" in data:
        data = data["arguments"]   # dạng tool-call thô {"name":..., "arguments": {...}}
    return data if isinstance(data, dict) else None


def _coerce_to_schema(data: dict, output_model) -> dict:
    """Ép mềm dict thô về đúng shape schema trước khi validate lại — vá lỗi model sinh gần đúng
    nhưng lệch kiểu/thiếu field, thay vì raise ngay và bỏ hẳn kết quả đó."""
    fixed = dict(data)
    for name, info in output_model.model_fields.items():
        if name not in fixed:
            continue
        val, ann = fixed[name], info.annotation

        if ann is str and isinstance(val, (list, dict)):
            fixed[name] = json.dumps(val, ensure_ascii=False) if isinstance(val, dict) else ", ".join(str(v) for v in val)
        elif getattr(ann, "__origin__", None) is list and isinstance(val, str):
            fixed[name] = [val]
        elif ann is int and isinstance(val, str) and val.strip().lstrip("-").isdigit():
            fixed[name] = int(val)

    return fixed


def _recover_from_failed(failed: str, output_model):
    data = _extract_json_block(failed)
    if data is None:
        return None
    try:
        return output_model.model_validate(data)
    except ValidationError:
        try:
            return output_model.model_validate(_coerce_to_schema(data, output_model))   # ← thêm bước ép mềm
        except Exception:
            return None

def _salvage_partial_array(failed: str, output_model, list_field: str):
    """Khi JSON bị cắt giữa chừng (hết token), tách các object ĐÃ ĐÓNG hoàn chỉnh
    trong mảng list_field, bỏ object dở dang cuối, dựng lại output_model với phần còn lại."""
    if not failed:
        return None
    start = failed.find(f'"{list_field}"')
    if start == -1:
        return None
    arr_start = failed.find('[', start)
    if arr_start == -1:
        return None

    items, depth, obj_start = [], 0, None
    for i, ch in enumerate(failed[arr_start:], start=arr_start):
        if ch == '{':
            if depth == 0:
                obj_start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and obj_start is not None:
                raw = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', failed[obj_start:i + 1])
                try:
                    items.append(json.loads(raw))
                except Exception:
                    pass
                obj_start = None

    if not items:
        return None
    try:
        return output_model.model_validate({list_field: items})
    except ValidationError:
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

    def invoke_structured(self, output_model, messages: list,
                        max_retries: int = 3, max_tokens: int = 4096, fallback=None, list_field: str = None):
        """3 lớp, tăng dần độ 'ép buộc':
        1) Tool-calling structured output (chuẩn nhất)
        2) json_mode + nhét thẳng JSON schema vào prompt
        3) Vớt raw text lỗi -> tách JSON -> ép mềm về schema -> validate lại
        Hết max_retries vẫn fail thì trả `fallback`, không crash graph."""
        base     = self._llm.bind(max_tokens=max_tokens)
        tool_llm = base.with_structured_output(output_model)
        json_llm = base.with_structured_output(output_model, method="json_mode")
        json_messages = messages + [{
            "role": "user",
            "content": "Trả về DUY NHẤT một JSON object đúng schema sau, không markdown, không giải thích:\n"
                        + json.dumps(output_model.model_json_schema(), ensure_ascii=False),
        }]

        for attempt in range(max_retries):
            use_json_mode = attempt >= 1
            llm  = json_llm if use_json_mode else tool_llm
            msgs = json_messages if use_json_mode else messages
            method_name = "json_mode" if use_json_mode else "tool_calling"

            try:
                result = llm.invoke(msgs)
                logger.info(f"invoke_structured [{output_model.__name__}] OK qua {method_name}, lần {attempt + 1}")
                return result
            except Exception as e:
                err_str = str(e)
                print(f"[invoke_structured] {output_model.__name__} attempt {attempt + 1} ({method_name}) lỗi: {err_str[:200]}")

                if "invalid_api_key" in err_str.lower() or "expired_api_key" in err_str.lower():
                    raise

                recovered = _recover_from_failed(_extract_failed(e), output_model)
                if recovered is None and list_field:
                    recovered = _salvage_partial_array(_extract_failed(e), output_model, list_field)
                    if recovered is not None:
                        print(f"[invoke_structured] {output_model.__name__} vớt được {len(getattr(recovered, list_field))} phần tử từ mảng bị cắt")

                if attempt < max_retries - 1:
                    m = re.search(r'try again in ([\d.]+)s', err_str)
                    time.sleep(float(m.group(1)) + 1 if m else 1)

        logger.error(f"invoke_structured [{output_model.__name__}] thất bại sau {max_retries} lần, dùng fallback")
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