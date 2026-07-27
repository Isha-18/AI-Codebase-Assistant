from mcp.server.fastmcp import FastMCP

from assistant_mcp.registry import register_components



class MCPServer:

    def __init__(self):

        self.server = FastMCP(
            name="AI Codebase Assistant",
            instructions="""
            AI assistant capable of understanding
            software repositories using Retrieval
            Augmented Generation (RAG).

            The assistant can:

            - Chat with repositories
            - Search classes
            - Search functions
            - Search files
            - Explain architecture
            - Review code
            - Provide repository statistics
            """
        )

        register_components(self.server)

    def run(self):
        self.server.run()


mcp_server = MCPServer()