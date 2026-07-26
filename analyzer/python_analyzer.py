import ast
from pathlib import Path


class PythonAnalyzer:
    """
    Extract structural metadata from Python source code.
    """

    def analyze(self, file_path: str) -> dict:

        path = Path(file_path)

        try:
            source = path.read_text(encoding="utf-8")
        except Exception:
            return {}

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return {}

        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.Import):
                imports.extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                imports.append(module)

        return {
            "language": "python",
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "line_count": len(source.splitlines()),
        }