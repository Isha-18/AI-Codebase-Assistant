import os
import tempfile

from git import Repo


def clone_repository(repo_url: str) -> str:
    """
    Clone a GitHub repository into a temporary directory.

    Args:
        repo_url: Public GitHub repository URL.

    Returns:
        Local path of the cloned repository.
    """

    temp_dir = tempfile.mkdtemp(prefix="repo_")

    Repo.clone_from(
        repo_url,
        temp_dir,
    )

    return temp_dir