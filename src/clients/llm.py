import logging
 
from mailbox import BabylMessage
import sys
import os

 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state import State, AgentProfile , StudyPlanOverview
from typing import Union, List
from langchain_core.messages import BaseMessage

from typing import List, Optional
from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.tools import BaseTool
from pydantic import BaseModel
from src.configs import env_config


logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with various LLM providers."""
    
    SUPPORTED_PROVIDERS = {
        # "openai": ChatOpenAI,
        # "anthropic": ChatAnthropic, 
        "google": ChatGoogleGenerativeAI,
        # "groq": ChatGroq
    }
    
    def __init__(self, model: str, api_provider: str):
        """
        Initialize the LLM client.
        
        Args:
            model: Model name to use
            api_provider: API provider ('openai', 'anthropic', 'google', 'groq')
            
        Raises:
            ValueError: If unsupported provider or missing configuration
        """
        if api_provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {api_provider}. Supported: {list(self.SUPPORTED_PROVIDERS.keys())}")
        
        self._llm = self._initialize_llm(model, api_provider)
        self.model = model
        self.api_provider = api_provider

    def _initialize_llm(self, model: str, api_provider: str):
        """Initialize the appropriate LLM based on provider."""
        try:
            # if api_provider == "openai":
            #     if not env_config.openai_api_key:
            #         raise ValueError("OpenAI API key not configured")
            #     return ChatOpenAI(model=model, openai_api_key=env_config.openai_api_key)
                
            # elif api_provider == "anthropic":
            #     if not env_config.anthropic_api_key:
            #         raise ValueError("Anthropic API key not configured")
            #     return ChatAnthropic(model=model, anthropic_api_key=env_config.anthropic_api_key)
                
            if api_provider == "google":
                if not env_config.google_api_key:
                    raise ValueError("Google API key not configured")
                return ChatGoogleGenerativeAI(model=model, google_api_key=env_config.google_api_key)
                
            # if api_provider == "groq":
            #     if not env_config.groq_api_key:
            #         raise ValueError("Groq API key not configured")
            #     return ChatGroq(model=model, groq_api_key=env_config.groq_api_key)
                
        except Exception as e:
            logger.error(f"Failed to initialize {api_provider} LLM: {e}")
            raise

    def invoke_with_retries(
        self,
        prompt: ChatPromptTemplate,
        max_tokens: int = 512,
        temperature: float = 0.7,
        llm_tools: List[BaseTool] = None,
        output_model: Optional[BaseModel] = None,
        num_retries: int = 2,
    ):
        """
        Invoke the LLM with retry logic.
        
        Args:
            prompt: Chat prompt template
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            llm_tools: List of tools to bind to the LLM
            output_model: Pydantic model for structured output
            num_retries: Number of retry attempts
            
        Returns:
            LLM response
            
        Raises:
            Exception: If all retry attempts fail
        """
        if llm_tools is None:
            llm_tools = []
            
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
                    logger.error(f"All {num_retries} attempts failed")
                    raise
                    
                logger.info(f"Retrying... {attempt + 2}/{num_retries}")

    async def ainvoke_with_retries(
        self,
        # prompt: ChatPromptTemplate,
        prompt: Union[ChatPromptTemplate, List[BaseMessage]],

        max_tokens: int = 2048,
        temperature: float = 0.7,
        llm_tools: List[BaseTool] = None,
        output_model: Optional[BaseModel] = None,
        num_retries: int = 2,
    ):
        if llm_tools is None:
            llm_tools = []

        llm = self._configure_llm(max_tokens, temperature, llm_tools, output_model)

        for attempt in range(num_retries):
            try:
                # print("ainvoke is running with ")

                if isinstance(prompt, list):  # list[BaseMessage]
                    print("list[BaseMessage]")

                    response = await llm.ainvoke(prompt)
                else:  # ChatPromptTemplate
                    print("ChatPromptTemplate")

                    chain = prompt | llm
                    response = await chain.ainvoke(input={})

                # logger.info(f"LLM_LLM gọi thành công ở lần thử thứ {attempt + 1}")
                # logger.debug(f" Đầu ra LLM:\n{response}")
                # print(f"✅ LLM phản hồi:\n{response.content if hasattr(response, 'content') else response}")
                
                return response

            except Exception as e:
                logger.error(f"❌ Lỗi ở lần thử thứ {attempt + 1}: {e}")

                if attempt == num_retries - 1:
                    logger.error(f"🚫 Tất cả {num_retries} lần gọi đều thất bại")

                    # Nếu có output_model, trả về bản rỗng để tránh gãy hệ thống
                    if output_model == StudyPlanOverview:
                        logger.warning("⚠️ Trả về kế hoạch học tập rỗng do lỗi LLM")
                        return StudyPlanOverview(
                            goal_summary="Không thể sinh kế hoạch",
                            strategy="Không có",
                            total_estimated_days=0,
                            available_days=0,
                            intensity_suggestion="Không xác định",
                            study_modules=[]
                        )

                    raise

                logger.info(f"🔁 Đang thử lại... ({attempt + 2}/{num_retries})")

    def _configure_llm(self, max_tokens: int, temperature: float, 
                      llm_tools: List[BaseTool], output_model: Optional[BaseModel]):
        """Configure the LLM with the specified parameters."""
        llm = self._llm.bind(max_tokens=max_tokens, temperature=temperature)
        
        if llm_tools:
            llm = llm.bind_tools(llm_tools)
            
        if output_model:
            llm = llm.with_structured_output(output_model)
            
        return llm

# Global LLM client instance
try:
    llm_client = LLMClient(
        model=env_config.model,
        api_provider=env_config.api_provider
    )
except Exception as e:
    logger.error(f"Failed to initialize global LLM client: {e}")
    llm_client = None

from langchain_core.messages import HumanMessage

try:
    llm_client = LLMClient(
        model=env_config.model,
        api_provider=env_config.api_provider
    )

    # Dùng trực tiếp llm bên trong LLMClient để test
    response = llm_client._llm.invoke([


        HumanMessage(content=" 1+ 1 = mấy ?")
    ])

    print("✅ LLM phản hồi:")
    print(response.content)

except Exception as e:
    logger.error(f"❌ Lỗi khởi tạo LLM client hoặc gọi LLM: {e}")
