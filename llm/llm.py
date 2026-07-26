from langchain_ollama import ChatOllama

from config.settings import settings

llm = ChatOllama(
    model=settings.LLM_MODEL
)