import git
from pydantic import Field
from .base import GitBaseModel

class GitDiff(GitBaseModel):
    other: str = Field(description="The branch/commit/tag to compare against")

class GitStatus(GitBaseModel):
    pass

class GitDiffUnstaged(GitBaseModel):
    pass

class GitDiffStaged(GitBaseModel):
    pass

class GitCommit(GitBaseModel):
    message: str

class GitAdd(GitBaseModel):
    files: list[str]

class GitReset(GitBaseModel):
    pass

def git_diff(repo: git.Repo, other: str) -> str:
    """Compare current HEAD with another branch/commit/tag"""
    try:
        return repo.git.diff("HEAD", other)
    except git.GitCommandError as e:
        if "fatal: bad revision" in str(e):
            return f"Invalid revision '{other}'"
        raise

def git_status(repo: git.Repo) -> str:
    return repo.git.status()

def git_diff_unstaged(repo: git.Repo) -> str:
    return repo.git.diff()

def git_diff_staged(repo: git.Repo) -> str:
    return repo.git.diff("--cached")

def git_commit(repo: git.Repo, message: str) -> str:
    commit = repo.index.commit(message)
    return f"Changes committed successfully with hash {commit.hexsha}"

def git_add(repo: git.Repo, files: list[str]) -> str:
    repo.index.add(files)
    return "Files staged successfully"

def git_reset(repo: git.Repo) -> str:
    repo.index.reset()
    return "All staged changes reset"