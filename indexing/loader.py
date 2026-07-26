from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader

from analyzer.repository_analyzer import RepositoryAnalyzer


analyzer = RepositoryAnalyzer()


def load_repository(repository_path: str):

    loader = DirectoryLoader(
        repository_path,
        glob="**/*",
        show_progress=True,
        silent_errors=True,
    )

    documents = loader.load()

    for document in documents:

        file_path = Path(document.metadata["source"])

        analysis = analyzer.analyze(str(file_path))

        metadata = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "extension": file_path.suffix,
            "language": analysis.get("language", ""),
            "line_count": analysis.get("line_count", 0),

            # Chroma doesn't support list metadata
            "classes": ",".join(
                analysis.get("classes", [])
            ),

            "functions": ",".join(
                analysis.get("functions", [])
            ),

            "imports": ",".join(
                analysis.get("imports", [])
            ),
        }

        document.metadata.update(metadata)

    return documents