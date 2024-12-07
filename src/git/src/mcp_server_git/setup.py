from pathlib import Path
import git
from .base import GitBaseModel

class GitInit(GitBaseModel):
    pass

def git_init(path: Path) -> str:
    git.Repo.init(path)
    return f"Initialized empty Git repository in {path}"