from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from core.llm import llm
from core.retriever import get_retriever


template = """
You are an AI Codebase Assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context, say:
"I couldn't find that information in the codebase."

Context:
{context}

Question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)

parser = StrOutputParser()


def ask_question(question: str):

    retriever = get_retriever()

    documents = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    chain = prompt | llm | parser

    return chain.invoke(
        {
            "context": context,
            "question": question
        }
    )