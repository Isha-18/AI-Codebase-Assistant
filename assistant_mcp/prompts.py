from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP):
    """
    Register reusable MCP prompts.

    Prompts help AI clients perform common
    repository-related tasks.
    """

    @mcp.prompt(
        name="explain_architecture",
        description="Explain the architecture of the repository."
    )
    def explain_architecture():

        return """
Explain the architecture of this repository.

Include:

- Overall architecture
- Folder structure
- Main modules
- Responsibilities of each layer
- Data flow
- Best practices followed
"""

    @mcp.prompt(
        name="code_review",
        description="Review the selected code."
    )
    def code_review():

        return """
Review this code like a Senior Software Engineer.

Focus on:

- Readability
- Maintainability
- SOLID Principles
- Design Patterns
- Bugs
- Performance
- Improvements
"""

    @mcp.prompt(
        name="api_review",
        description="Review REST APIs."
    )
    def api_review():

        return """
Review the APIs.

Check for:

- REST conventions
- Request validation
- Response structure
- Error handling
- Security
- Naming consistency
"""

    @mcp.prompt(
        name="generate_readme",
        description="Generate a professional README."
    )
    def generate_readme():

        return """
Generate a professional GitHub README.

Include:

- Project Overview
- Features
- Architecture
- Folder Structure
- Installation
- Usage
- Tech Stack
- Future Improvements
"""

    @mcp.prompt(
        name="generate_tests",
        description="Generate unit tests."
    )
    def generate_tests():

        return """
Generate production-quality unit tests.

Cover:

- Happy Path
- Edge Cases
- Invalid Inputs
- Exceptions
"""

    @mcp.prompt(
        name="find_bugs",
        description="Find possible bugs."
    )
    def find_bugs():

        return """
Analyze the repository.

Find:

- Logical bugs
- Runtime issues
- Null checks
- Resource leaks
- Error handling issues
"""

    @mcp.prompt(
        name="repository_structure",
        description="Explain repository structure."
    )
    def repository_structure():

        return """
Explain the repository structure.

Describe:

- Purpose of each folder
- Responsibilities
- Dependencies
- Overall project organization
"""

    @mcp.prompt(
        name="authentication_flow",
        description="Explain authentication flow."
    )
    def authentication_flow():

        return """
Explain the authentication flow.

Include:

- Authentication mechanism
- Authorization
- Security
- Request flow
- Possible improvements
"""