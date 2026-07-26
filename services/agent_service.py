from langchain_core.messages import HumanMessage

from llm.llm import llm
from tools import TOOLS


class AgentService:

    def __init__(self):

        self.llm = llm.bind_tools(TOOLS)

    def chat(self, question: str):

        response = self.llm.invoke(
            [
                HumanMessage(content=question)
            ]
        )

        # If the model answered directly
        if not response.tool_calls:
            return {
                "answer": response.content,
                "sources": [],
            }

        answers = []

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            tool = next(
                t
                for t in TOOLS
                if t.name == tool_name
            )

            tool_result = tool.invoke(tool_args)

            answers.append(tool_result)

        return {
            "answer": "\n\n".join(answers),
            "sources": [],
        }