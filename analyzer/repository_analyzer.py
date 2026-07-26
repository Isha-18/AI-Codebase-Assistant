from pathlib import Path

from analyzer.python_analyzer import PythonAnalyzer


class RepositoryAnalyzer:

    def __init__(self):

        self.python_analyzer = PythonAnalyzer()

    def analyze(self, file_path: str) -> dict:

        extension = Path(file_path).suffix.lower()

        if extension == ".py":
            return self.python_analyzer.analyze(file_path)

        return {}