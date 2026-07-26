from langchain.tools import tool

from services.rag_service import RAGService

rag_service = RAGService()


@tool
def codebase_chat(question: str) -> str:
    """
    Use this tool whenever the user asks about:

    - how the code works
    - authentication
    - APIs
    - repository architecture
    - implementation details
    - explain code
    - summarize files
    - code flow
    - debugging
    - repository questions

    Never answer these questions from your own knowledge.
    Always search the repository first.
    """

    result = rag_service.chat(question)
    print("******** USING RAG TOOL ********")

    return result["answer"]