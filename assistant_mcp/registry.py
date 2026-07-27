from assistant_mcp.tools import register_tools
from assistant_mcp.resources import register_resources
from assistant_mcp.prompts import register_prompts

from mcp.server.fastmcp import FastMCP



def register_components(server: FastMCP):
    """
    Register all MCP components.
    """

    register_tools(server)

    register_resources(server)

    register_prompts(server)