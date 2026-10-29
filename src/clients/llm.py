"""Provider-aware LLM calls; public agent entry points remain compatible."""
from __future__ import annotations

import asyncio, copy, itertools, json, logging, os, random, re, sys, threading, time
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from functools import lru_cache

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, ValidationError
from src.configs import env_config
from src.clients.api_logger import ApiLogHandler

logger = logging.getLogger(__name__)
_key_lock = threading.Lock()
_key_counter = itertools.count(random.randrange(max(1, len(env_config.groq_api_keys))))


# def _next_groq_key() -> str:
#     keys = env_config.groq_api_keys
#     if not keys:
#         raise ValueError("Thiếu GROQ_API_KEY trong src/.env")
#     if getattr(env_config, "groq_key_strategy", "round_robin") == "fixed":
#         return keys[0]
#     with _key_lock:
#         return keys[next(_key_counter) % len(keys)]

def _next_groq_key() -> str:
    keys = env_config.groq_api_keys
    if not keys:
        raise ValueError("Thiếu GROQ_API_KEY trong src/.env")

    if getattr(env_config, "groq_key_strategy", "round_robin") == "fixed":
        key = keys[0]
    else:
        with _key_lock:
            key = keys[next(_key_counter) % len(keys)]

    if key.endswith("Ps5"):
        number = 1
    elif key.endswith("Go"):
        number = 2
    elif key.endswith("WU5"):
        number = 3
    elif key.endswith("Nex"):
        number = 4
    elif key.endswith("Xjx"):
        number = 5
    elif key.endswith("Oy6"):
        number = 6
    else:
        number = "không xác định"
    # print(f" strategy={getattr(env_config, 'groq_key_strategy', None)}, so_key={len(keys)}", flush=True)
    # print(f" 🔑🔑 API_KEY_RUNNING = {number}", flush=True)
    return key

def _rotating_groq_clients():
    from groq import Groq, AsyncGroq

    class RotGroq(Groq):
        @property
        def auth_headers(self):
            return {"Authorization": f"Bearer {_next_groq_key()}"}

    class RotAsyncGroq(AsyncGroq):
        @property
        def auth_headers(self):
            return {"Authorization": f"Bearer {_next_groq_key()}"}

    options = dict(api_key=env_config.groq_api_keys[0],
                   timeout=env_config.llm_timeout_seconds, max_retries=0)
    return RotGroq(**options).chat.completions, RotAsyncGroq(**options).chat.completions


def _extract_failed(error) -> str:
    body = getattr(error, "body", None)
    if isinstance(body, dict):
        return body.get("failed_generation") or (body.get("error") or {}).get("failed_generation") or ""
    return ""


def _extract_json_block(text: str):
    """Decode objects without greedy regexes that swallow multiple JSON blocks."""
    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", text or ""):
        try:
            data, _ = decoder.raw_decode(text[match.start():])
        except ValueError:
            continue
        if isinstance(data, dict):
            if "name" in data and "arguments" in data:
                data = data["arguments"]
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except ValueError:
                        continue
            if isinstance(data, dict):
                return data
    return None


def _validated(data, output_model):
    result = output_model.model_validate(data)
    if "tin_nhan" in output_model.model_fields and not result.tin_nhan.strip():
        raise ValueError("Model trả về tin_nhan rỗng")
    return result


def _recover_from_failed(text, output_model):
    data = _extract_json_block(text)
    if data is not None:
        try:
            return _validated(data, output_model)
        except (ValidationError, ValueError):
            pass
    return None


def _salvage_partial_array(text, output_model, list_field):
    """Only used when the caller explicitly opts into partial array recovery."""
    match = re.search(r'"' + re.escape(list_field) + r'"\s*:\s*\[', text or "")
    if not match:
        return None
    decoder, items, pos = json.JSONDecoder(), [], match.end()
    while pos < len(text):
        while pos < len(text) and text[pos] in " \r\n\t,":
            pos += 1
        try:
            item, length = decoder.raw_decode(text[pos:])
        except ValueError:
            break
        items.append(item)
        pos += length
    if items:
        try:
            return _validated({list_field: items}, output_model)
        except (ValidationError, ValueError):
            pass
    return None


def build_prompt_messages(prompt_path, values: dict) -> list[dict]:
    system, marker, user = prompt_path.read_text(encoding="utf-8").partition(
        "THÔNG TIN CHI TIẾT ĐƯỢC CUNG CẤP"
    )
    if not marker:
        raise ValueError(f"Thiếu dòng phân cách trong {prompt_path.name}")
    for key, value in values.items():
        user = user.replace("{" + key + "}", str(value))
    return [{"role": "system", "content": system.strip()},
            {"role": "user", "content": user.strip()}]


@lru_cache(maxsize=128)
def _strict_schema(output_model):
    """Never close dynamic dictionaries: doing so would discard schedule keys."""
    schema = copy.deepcopy(output_model.model_json_schema())

    def visit(node):
        if isinstance(node, list):
            return all(visit(value) for value in node)
        if not isinstance(node, dict):
            return True
        if node.get("type") == "object":
            if "properties" not in node or node.get("additionalProperties") not in (None, False):
                return False
            node["additionalProperties"] = False
            node["required"] = list(node["properties"])
        node.pop("default", None)
        return all(visit(value) for value in node.values())

    return schema if visit(schema) else None


def _raw_text(raw):
    content = getattr(raw, "content", "")
    if isinstance(content, str):
        return content
    return "".join(block.get("text", "") for block in content
                   if isinstance(block, dict) and block.get("type") == "text")


def _recover_raw(raw, output_model):
    for call in getattr(raw, "tool_calls", []) or []:
        try:
            return _validated(call["args"], output_model)
        except (KeyError, ValidationError, ValueError):
            continue
    return _recover_from_failed(_raw_text(raw), output_model)


def _status(error):
    return getattr(error, "status_code", None)


def _transient(error):
    status = _status(error)
    return status in (408, 409, 429) or (isinstance(status, int) and status >= 500) or (
        isinstance(error, (TimeoutError, ConnectionError))
        or type(error).__name__ in ("APITimeoutError", "APIConnectionError")
    )


def _retry_delay(error, attempt):
    headers = getattr(getattr(error, "response", None), "headers", {}) or {}
    value = headers.get("retry-after")
    if value:
        try:
            return max(0.0, float(value))
        except ValueError:
            try:
                return max(0.0, (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds())
            except (ValueError, TypeError):
                pass
    match = re.search(r"try again in ([\d.]+)s", str(error), re.I)
    if match:
        return float(match.group(1)) + 0.1
    return min(8.0, 2 ** attempt) + random.uniform(0, 0.25)

@lru_cache(maxsize=None)
def _retrying(base):
    """Lớp con thử lại lỗi tạm thời (429/5xx/timeout/kết nối) cho lời gọi trực tiếp `_llm`.
    `inner_retries=0` ở bản sao dùng cho invoke_structured/invoke_with_retries (chúng tự thử lại)."""
    class Retrying(base):
        inner_retries: int = 2

        def _generate(self, *args, **kwargs):
            for attempt in range(self.inner_retries + 1):
                try:
                    return super()._generate(*args, **kwargs)
                except Exception as error:
                    if attempt >= self.inner_retries or not _transient(error):
                        raise
                    time.sleep(_retry_delay(error, attempt))

        async def _agenerate(self, *args, **kwargs):
            for attempt in range(self.inner_retries + 1):
                try:
                    return await super()._agenerate(*args, **kwargs)
                except Exception as error:
                    if attempt >= self.inner_retries or not _transient(error):
                        raise
                    await asyncio.sleep(_retry_delay(error, attempt))

    Retrying.__name__ = f"Retrying{base.__name__}"
    return Retrying

class LLMClient:
    def __init__(self, model: str, api_provider: str = None):
        self.model = model
        self.api_provider = api_provider or env_config.api_provider
        self._llm = self._initialize_llm()

    @property
    def _luna(self):
        return self.model.removeprefix("openai/") == "gpt-6-luna"

    def _initialize_llm(self):
        common = dict(model=self.model, timeout=env_config.llm_timeout_seconds, max_retries=0,
                      callbacks=[ApiLogHandler(self.api_provider, self.model)])
        if self.api_provider == "groq":
            from langchain_groq import ChatGroq as _ChatGroq
            ChatGroq = _retrying(_ChatGroq)
            if not env_config.groq_api_keys:
                raise ValueError("Thiếu GROQ_API_KEY trong src/.env")
            client, async_client = _rotating_groq_clients()
            effort = env_config.reasoning_effort
            # ChatGroq 0.3.5 restricts its field to none/default. The current
            # Groq API accepts low/medium/high for OSS; SDK extra_body passes
            # these values without relying on that outdated local enum.
            extra = {"model_kwargs": {"extra_body": {"reasoning_effort": effort}}} if effort else {}
            return ChatGroq(**common, groq_api_key=env_config.groq_api_keys[0],
                            client=client, async_client=async_client, **extra)
        if self.api_provider not in ("openai", "openrouter"):
            raise ValueError(f"api_provider không hỗ trợ: {self.api_provider}")
        from langchain_openai import ChatOpenAI as _ChatOpenAI
        ChatOpenAI = _retrying(_ChatOpenAI)
        key = (env_config.openrouter_api_key if self.api_provider == "openrouter"
               else env_config.openai_api_key)
        if not key:
            raise ValueError(f"Thiếu API key cho {self.api_provider}")
        # Luna Chat Completions only supports function calling with reasoning=none.
        # Keep the exposed _llm safe for graph nodes that call bind_tools directly.
        effort = "none" if self._luna else env_config.reasoning_effort
        extra = {}
        if self.api_provider == "openrouter":
            extra["base_url"] = "https://openrouter.ai/api/v1"
            body = {}
            if effort:
                body["reasoning"] = {"effort": effort}
            if env_config.openrouter_provider:
                body["provider"] = {"order": [env_config.openrouter_provider],
                                    "allow_fallbacks": True}
            if env_config.llm_cache_key:
                body["prompt_cache_key"] = env_config.llm_cache_key
            if body:
                extra["extra_body"] = body
        else:
            if effort:
                extra["reasoning_effort"] = effort
            if env_config.llm_cache_key:
                extra["extra_body"] = {"prompt_cache_key": env_config.llm_cache_key}
        return ChatOpenAI(**common, api_key=key, **extra)

    def _request_model(self, max_tokens, temperature=None, *, function_calling=False):
        # Model fields survive bind_tools/with_structured_output; bound kwargs may not.
        update = {"max_tokens": max_tokens, "inner_retries": 0}
        if temperature is not None and not self._luna:
            update["temperature"] = temperature
        if self._luna:
            effort = "none" if function_calling else (env_config.reasoning_effort or "low")
            if self.api_provider == "openrouter":
                body = copy.deepcopy(getattr(self._llm, "extra_body", None) or {})
                body["reasoning"] = {"effort": effort}
                update["extra_body"] = body
            else:
                update["reasoning_effort"] = effort
        return self._llm.model_copy(update=update)

    def _native_schema(self, output_model):
        supported = "gpt-oss" in self.model or self.model.removeprefix("openai/").startswith(
            ("gpt-4o", "gpt-4.1", "gpt-5", "gpt-6")
        )
        return _strict_schema(output_model) if supported else None

    def _structured_runner(self, output_model, max_tokens, method):
        if method == "json_schema":
            schema = self._native_schema(output_model)
            if schema is None:
                raise ValueError("Schema/model không hỗ trợ native strict JSON schema")
            model = self._request_model(max_tokens)
            if self.api_provider == "openrouter":
                body = copy.deepcopy(getattr(model, "extra_body", None) or {})
                provider = body.setdefault("provider", {})
                provider["require_parameters"] = True
                model = model.model_copy(update={"extra_body": body})
            # Send the native format directly: works with the pinned older ChatGroq.
            return model.bind(response_format={"type": "json_schema", "json_schema": {
                "name": output_model.__name__, "strict": True, "schema": schema}})
        return self._request_model(max_tokens, function_calling=True).with_structured_output(
            output_model, method="function_calling", include_raw=True)

    def _configure_llm(self, max_tokens, temperature, llm_tools, output_model):
        if llm_tools and output_model:
            raise ValueError("Gọi tools và sinh output_model ở hai bước riêng; không bind chồng làm mất tools.")
        if output_model:
            # Use the same validation/retry path as collect and planning.
            return RunnableLambda(
                lambda prompt: self.invoke_structured(output_model, self._messages(prompt),
                                                       max_tokens=max_tokens),
                afunc=lambda prompt: self.ainvoke_structured(output_model, self._messages(prompt),
                                                             max_tokens=max_tokens),
            )
        model = self._request_model(max_tokens, temperature, function_calling=bool(llm_tools))
        return model.bind_tools(llm_tools) if llm_tools else model

    @staticmethod
    def _messages(prompt):
        if isinstance(prompt, list):
            return prompt
        if hasattr(prompt, "to_messages"):
            return prompt.to_messages()
        if isinstance(prompt, ChatPromptTemplate):
            return prompt.invoke({}).to_messages()
        return [HumanMessage(content=str(prompt))]

    def _prepare_messages(self, messages):
        """Opt-in stable-prefix breakpoints for Luna; never pad or rewrite text."""
        messages = copy.deepcopy(self._messages(messages))
        if not self._luna or not env_config.llm_explicit_cache:
            return messages
        for message in messages:
            role = message.get("role") if isinstance(message, dict) else message.type
            if role not in ("system", "developer"):
                break
            content = message.get("content") if isinstance(message, dict) else message.content
            if not isinstance(content, str) or not content:
                continue
            blocks = [{"type": "text", "text": content,
                       "prompt_cache_breakpoint": {"mode": "explicit"}}]
            if isinstance(message, dict):
                message["content"] = blocks
            else:
                message.content = blocks
        return messages

    def _report(self, raw, elapsed, method, attempt):
        usage = getattr(raw, "usage_metadata", None) or {}
        metadata = getattr(raw, "response_metadata", None) or {}
        token_usage = metadata.get("token_usage") or metadata.get("usage") or {}
        details = usage.get("input_token_details") or {}
        raw_details = token_usage.get("prompt_tokens_details") or token_usage.get("input_tokens_details") or {}
        cached = details.get("cache_read", raw_details.get("cached_tokens"))
        written = details.get("cache_creation", raw_details.get("cache_write_tokens",
                             raw_details.get("cache_creation_tokens")))
        reasoning = (usage.get("output_token_details") or {}).get(
            "reasoning", (token_usage.get("completion_tokens_details") or {}).get("reasoning_tokens"))
        logger.info("LLM provider=%s model=%s method=%s attempt=%d seconds=%.3f input=%s output=%s cache_read=%s cache_write=%s reasoning=%s finish=%s",
                    self.api_provider, self.model, method, attempt, elapsed,
                    usage.get("input_tokens", token_usage.get("prompt_tokens")),
                    usage.get("output_tokens", token_usage.get("completion_tokens")),
                    cached if cached is not None else "not_reported",
                    written if written is not None else "not_reported",
                    reasoning if reasoning is not None else "not_reported",
                    metadata.get("finish_reason"))

    def invoke_with_retries(self, prompt, max_tokens=4096, temperature=1,
                            llm_tools=None, output_model=None, num_retries=1):
        if output_model and not llm_tools:
            return self.invoke_structured(output_model, self._messages(prompt),
                                          max_retries=num_retries, max_tokens=max_tokens)
        llm = self._configure_llm(max_tokens, temperature, llm_tools or [], output_model)
        for attempt in range(max(1, num_retries)):
            start = time.perf_counter()
            try:
                response = llm.invoke(self._prepare_messages(prompt))
                self._report(response, time.perf_counter() - start, "tools" if llm_tools else "text", attempt + 1)
                return response
            except Exception as error:
                if not _transient(error) or attempt + 1 >= max(1, num_retries):
                    raise
                time.sleep(_retry_delay(error, attempt))

    async def ainvoke_with_retries(self, prompt, max_tokens=4096, temperature=1,
                                   llm_tools=None, output_model=None, num_retries=1):
        if output_model and not llm_tools:
            return await self.ainvoke_structured(output_model, self._messages(prompt),
                                                 max_retries=num_retries, max_tokens=max_tokens)
        llm = self._configure_llm(max_tokens, temperature, llm_tools or [], output_model)
        for attempt in range(max(1, num_retries)):
            start = time.perf_counter()
            try:
                response = await llm.ainvoke(self._prepare_messages(prompt))
                self._report(response, time.perf_counter() - start, "tools" if llm_tools else "text", attempt + 1)
                return response
            except Exception as error:
                if not _transient(error) or attempt + 1 >= max(1, num_retries):
                    raise
                await asyncio.sleep(_retry_delay(error, attempt))

    def invoke_structured(self, output_model, messages: list, max_retries=3,
                          max_tokens=4096, fallback=None, list_field=None):
        """Native strict for compatible schemas; explicit function calling otherwise.

        max_retries retains its old meaning: total application-level attempts.
        Authentication/configuration failures raise; exhausted transient/validation
        failures return the caller's fallback. No semantic values are invented.
        """
        messages = self._prepare_messages(messages)
        method = "json_schema" if self._native_schema(output_model) is not None else "function_calling"
        for attempt in range(max(1, max_retries)):
            raw = None
            start = time.perf_counter()
            try:
                runner = self._structured_runner(output_model, max_tokens, method)
                response = runner.invoke(messages)
                if method == "json_schema":
                    raw = response
                else:
                    raw = response["raw"]
                self._report(raw, time.perf_counter() - start, method, attempt + 1)
                metadata = getattr(raw, "response_metadata", None) or {}
                if metadata.get("finish_reason") == "length":
                    raise ValueError("Output bị cắt do hết token; tăng max_tokens hoặc giảm reasoning.")
                if method == "function_calling":
                    if response.get("parsing_error"):
                        raise response["parsing_error"]
                    if response.get("parsed") is None:
                        raise ValueError("Không có kết quả structured output")
                    return _validated(response["parsed"], output_model)
                return _validated(json.loads(_raw_text(raw)), output_model)
            except Exception as error:
                if type(error).__name__ == "LengthFinishReasonError":
                    # OpenAI's parse helper can raise before LangChain returns raw.
                    completion = getattr(error, "completion", None)
                    if completion and completion.choices:
                        raw = AIMessage(content=completion.choices[0].message.content or "",
                                        response_metadata={"finish_reason": "length",
                                                           "token_usage": completion.usage.model_dump() if completion.usage else {}})
                        self._report(raw, time.perf_counter() - start, method, attempt + 1)
                status = _status(error)
                if status in (401, 403) or (status is not None and not _transient(error)):
                    # A rejected native schema may use the less restrictive tool API.
                    text = str(error).lower()
                    # if status == 400 and method == "json_schema" and any(...):
                    if status == 400 and method == "json_schema" and any(k in text for k in ("schema", "response_format", "structured", "strict", "json")):
                        method = "function_calling"
                    elif status == 400 and "tool_use_failed" in text:
                        pass
                    else:
                        raise
                elif (type(error).__name__ != "LengthFinishReasonError"
                      and not _transient(error) and not isinstance(error, (ValueError, ValidationError))):
                    raise
                finish = (getattr(raw, "response_metadata", None) or {}).get("finish_reason")
                recovered = None if finish == "length" else (
                    _recover_raw(raw, output_model) if raw is not None else
                    _recover_from_failed(_extract_failed(error), output_model)
                )
                if recovered is not None:
                    logger.warning("Recovered validated %s without another API call", output_model.__name__)
                    return recovered
                if list_field and finish == "length":
                    recovered = _salvage_partial_array(_raw_text(raw), output_model, list_field)
                    if recovered is not None:
                        logger.warning("Returning explicitly requested partial array: %s", list_field)
                        return recovered
                logger.warning("LLM failed provider=%s model=%s method=%s attempt=%d error_type=%s status=%s error=%s",
                               self.api_provider, self.model, method, attempt + 1, type(error).__name__, status, str(error)[:300])
                if attempt + 1 >= max(1, max_retries):
                    break
                if _transient(error):
                    delay = _retry_delay(error, attempt)
                    logger.info("Retry after %.2f seconds", delay)
                    time.sleep(delay)
                elif finish == "length":
                    # Do not retry the identical truncated request.
                    break
                elif status != 400:
                    messages = messages + [{"role": "user", "content":
                        "Kết quả trước không hợp lệ. Trả đầy đủ cấu trúc yêu cầu, đúng kiểu dữ liệu; không suy đoán thông tin còn thiếu."}]
        logger.error("Structured output failed: %s; returning fallback", output_model.__name__)
        return fallback

    async def ainvoke_structured(self, output_model, messages: list, **kwargs):
        # Reuse exactly the same recovery semantics without blocking the event loop.
        return await asyncio.to_thread(self.invoke_structured, output_model, messages, **kwargs)


try:
    llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)
except Exception:
    logger.error("Failed to initialize global LLM client; check provider/model configuration")
    llm_client = None


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description="LLM latency/token smoke test")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--prefix-file", type=Path, help="Real reusable system instructions; never padded")
    args = parser.parse_args()
    if not 1 <= args.repeat <= 20:
        parser.error("--repeat must be between 1 and 20")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if llm_client is None:
        raise SystemExit("Không khởi tạo được LLM client")
    messages = []
    if args.prefix_file:
        messages.append({"role": "system", "content": args.prefix_file.read_text(encoding="utf-8")})
    messages.append({"role": "user", "content": "năm 2022 ai là tổng thống nước mỹ"})
    for run in range(args.repeat):
        print(f"Run {run + 1}/{args.repeat}", flush=True)
        response = llm_client.invoke_with_retries(messages, max_tokens=256)
        print(response.content)
