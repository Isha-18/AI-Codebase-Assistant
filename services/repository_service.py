from retrieval.vectorstore import get_vectorstore


class RepositoryService:

    def __init__(self):
        self.vectorstore = get_vectorstore()

    def _documents(self):
        collection = self.vectorstore._collection
        result = collection.get(include=["metadatas"])
        return result["metadatas"]

    def _split_metadata(self, value: str):
        """
        Convert comma-separated metadata into a list.
        """
        if not value:
            return []

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    def get_classes(self):

        classes = set()

        for metadata in self._documents():

            classes.update(
                self._split_metadata(
                    metadata.get("classes", "")
                )
            )

        return sorted(classes)

    def get_functions(self):

        functions = set()

        for metadata in self._documents():

            functions.update(
                self._split_metadata(
                    metadata.get("functions", "")
                )
            )

        return sorted(functions)

    def get_imports(self):

        imports = set()

        for metadata in self._documents():

            imports.update(
                self._split_metadata(
                    metadata.get("imports", "")
                )
            )

        return sorted(imports)

    def get_stats(self):

        metadatas = self._documents()

        classes = set()
        functions = set()

        for metadata in metadatas:

            classes.update(
                self._split_metadata(
                    metadata.get("classes", "")
                )
            )

            functions.update(
                self._split_metadata(
                    metadata.get("functions", "")
                )
            )

        return {
            "total_documents": len(metadatas),
            "total_classes": len(classes),
            "total_functions": len(functions),
        }