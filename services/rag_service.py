from pathlib import Path
import re
from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm.llm import llm
from retrieval.retriever import get_retriever
from config.settings import settings


class RAGService:
    """
    Handles Retrieval-Augmented Generation for the
    indexed repository.

    Retrieval uses:
    1. Semantic similarity
    2. Exact file matching
    3. Exact class matching
    4. Exact function matching
    5. Code-content matching
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

    # ---------------------------------------------------------
    # EXTRACT CODE TERMS
    # ---------------------------------------------------------

    def _extract_terms(self, question: str) -> list[str]:
        """
        Extract useful code identifiers from the question.
        """

        terms = re.findall(
            r"\b[A-Za-z_][A-Za-z0-9_]*\b",
            question,
        )

        # Ignore common natural-language words.
        stop_words = {
            "the",
            "this",
            "that",
            "what",
            "where",
            "how",
            "why",
            "which",
            "when",
            "does",
            "do",
            "is",
            "are",
            "and",
            "or",
            "for",
            "from",
            "with",
            "explain",
            "show",
            "find",
            "code",
            "class",
            "function",
            "file",
            "method",
            "used",
            "use",
        }

        return [
            term.lower()
            for term in terms
            if term.lower() not in stop_words
            and len(term) > 2
        ]

    # ---------------------------------------------------------
    # SCORE DOCUMENT
    # ---------------------------------------------------------

    def _score_document(
        self,
        document: Document,
        terms: list[str],
    ) -> int:

        metadata = document.metadata

        file_path = str(
            metadata.get(
                "file_path",
                metadata.get("source", ""),
            )
        ).lower()

        file_name = str(
            metadata.get(
                "file_name",
                "",
            )
        ).lower()

        classes = str(
            metadata.get(
                "classes",
                "",
            )
        ).lower()

        functions = str(
            metadata.get(
                "functions",
                "",
            )
        ).lower()

        imports = str(
            metadata.get(
                "imports",
                "",
            )
        ).lower()

        content = document.page_content.lower()

        score = 0

        for term in terms:

            # Exact function match
            if term in functions:
                score += 10

            # Exact class match
            if term in classes:
                score += 10

            # File name match
            if term in file_name:
                score += 8

            # File path match
            if term in file_path:
                score += 5

            # Import match
            if term in imports:
                score += 3

            # Code content match
            if term in content:
                score += 2

        return score

    # ---------------------------------------------------------
    # RERANK DOCUMENTS
    # ---------------------------------------------------------

    def _rerank_documents(
        self,
        documents: List[Document],
        question: str,
    ) -> List[Document]:

        terms = self._extract_terms(question)

        scored_documents = []

        for document in documents:

            score = self._score_document(
                document,
                terms,
            )

            scored_documents.append(
                (score, document)
            )

        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in scored_documents
        ]

    # ---------------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------------

    def _remove_duplicate_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:

        seen = set()
        unique_documents = []

        for document in documents:

            file_path = document.metadata.get(
                "file_path",
                document.metadata.get(
                    "source",
                    "Unknown",
                ),
            )

            content = document.page_content.strip()

            key = (
                str(file_path),
                content,
            )

            if key in seen:
                continue

            seen.add(key)
            unique_documents.append(document)

        return unique_documents

    # ---------------------------------------------------------
    # RETRIEVE
    # ---------------------------------------------------------

    def _retrieve_documents(
        self,
        question: str,
    ) -> List[Document]:

        documents = self.retriever.invoke(
            question
        )

        documents = self._remove_duplicate_documents(
            documents
        )

        documents = self._rerank_documents(
            documents,
            question,
        )

        return documents[:settings.RETRIEVAL_TOP_K]

    # ---------------------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------------------

    def _build_context(
        self,
        documents: List[Document],
    ):

        context_parts = []
        sources = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = document.metadata

            file_path = metadata.get(
                "file_path",
                metadata.get(
                    "source",
                    "Unknown",
                ),
            )

            file_name = metadata.get(
                "file_name",
                "Unknown",
            )

            language = metadata.get(
                "language",
                "Unknown",
            )

            classes = metadata.get(
                "classes",
                "",
            )

            functions = metadata.get(
                "functions",
                "",
            )

            imports = metadata.get(
                "imports",
                "",
            )

            if file_path not in sources:
                sources.append(file_path)

            context_parts.append(
                f"""
SOURCE {index}

File:
{file_path}

File Name:
{file_name}

Language:
{language}

Classes:
{classes or "None"}

Functions:
{functions or "None"}

Imports:
{imports or "None"}

Code:
----------------------------------
{document.page_content}
----------------------------------
"""
            )

        return "\n".join(context_parts), sources

    # ---------------------------------------------------------
    # CHAT
    # ---------------------------------------------------------

    def chat(self, question: str):

        documents = self._retrieve_documents(
            question
        )

        if not documents:

            return {
                "answer": (
                    "I could not find relevant code "
                    "in the indexed repository."
                ),
                "sources": [],
            }

        context, sources = self._build_context(
            documents
        )

        answer = self.chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        return {
            "answer": answer,
            "sources": sources,
        }