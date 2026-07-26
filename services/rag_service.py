from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm.llm import llm
from retrieval.retriever import get_retriever


class RAGService:
    """
    Handles Retrieval-Augmented Generation (RAG)
    for answering questions about the indexed repository.
    """

    def __init__(self):

        prompt_path = Path("prompts/system_prompt.txt")

        template = prompt_path.read_text(
            encoding="utf-8"
        )

        self.prompt = ChatPromptTemplate.from_template(
            template
        )

        self.parser = StrOutputParser()

        self.retriever = get_retriever()

        self.chain = (
            self.prompt
            | llm
            | self.parser
        )

    def chat(self, question: str):

        documents = self.retriever.invoke(question)

        context = ""

        sources = []

        for document in documents:

            source = document.metadata.get(
                "file_path",
                document.metadata.get(
                    "source",
                    "Unknown",
                ),
            )

            sources.append(source)

            context += f"""
File:
{source}

----------------------------------

{document.page_content}

==================================

"""

        answer = self.chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        return {
            "answer": answer,
            "sources": list(dict.fromkeys(sources)),
        }