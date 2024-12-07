import git
from pydantic import Field
from .base import GitBaseModel

class GitLog(GitBaseModel):
    max_count: int = 10

class GitCreateBranch(GitBaseModel):
    branch_name: str
    base_branch: str | None = None

class GitSwitch(GitBaseModel):
    branch_name: str
    create_branch: bool = Field(default=False, description="Create new branch if it doesn't exist (-c)")

def git_log(repo: git.Repo, max_count: int = 10) -> list[str]:
    commits = list(repo.iter_commits(max_count=max_count))
    log = []
    for commit in commits:
        log.append(
            f"Commit: {commit.hexsha}\n"
            f"Author: {commit.author}\n"
            f"Date: {commit.authored_datetime}\n"
            f"Message: {commit.message}\n"
        )
    return log

def git_create_branch(repo: git.Repo, branch_name: str, base_branch: str | None = None) -> str:
    if base_branch:
        base = repo.refs[base_branch]
    else:
        base = repo.active_branch

    repo.create_head(branch_name, base)
    return f"Created branch '{branch_name}' from '{base.name}'"

def git_switch(repo: git.Repo, branch_name: str, create_branch: bool = False) -> str:
    try:
        if create_branch:
            repo.git.switch(branch_name, c=True)
            return f"Created and switched to new branch '{branch_name}'"
        else:
            repo.git.switch(branch_name)
            return f"Switched to branch '{branch_name}'"
    except git.GitCommandError as e:
        if "did not match any file(s) known to git" in str(e):
            return f"Branch '{branch_name}' does not exist. Use create_branch=True to create it."
        raise