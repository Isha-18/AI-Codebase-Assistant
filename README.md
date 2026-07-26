Version 2 - Architecture Refactor

Major Improvements

• Introduced a service layer to separate API endpoints from business logic.
• Added IndexingService, ChatService, RepositoryService and RAGService.
• Replaced inline route logic with reusable service classes.
• Introduced Pydantic request and response models for cleaner APIs.
• Externalized prompts into prompt files.
• Enhanced RAG pipeline with source citations and metadata-aware context.
• Added repository analysis using Python AST to extract classes, functions and imports.
• Stored repository metadata inside ChromaDB for future code intelligence features.
• Added LangChain Tools wrapping repository operations and RAG.
• Refactored project into a production-ready modular architecture following SOLID principles.
• Prepared the codebase for Agent workflows, MCP integration and LangGraph.