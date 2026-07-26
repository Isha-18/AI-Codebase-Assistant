from services.agent_service import AgentService


class ChatService:

    def __init__(self):

        self.agent = AgentService()

    def chat(self, question: str):

        return self.agent.chat(question)