from pydantic import BaseModel, Field
import git
from .base import GitBaseModel

class GitFetch(GitBaseModel):
    remote: str = Field(default="origin", description="Remote name to fetch from")

class GitPull(GitBaseModel):
    remote: str = Field(default="origin", description="Remote to pull from")
    branch: str | None = Field(default=None, description="Branch to pull (default: current branch)")

class GitPush(GitBaseModel):
    remote: str = Field(default="origin", description="Remote to push to")
    branch: str | None = Field(default=None, description="Branch to push (default: current branch)")
    set_upstream: bool = Field(default=False, description="Set up tracking branch")

class GitRemoteAdd(GitBaseModel):
    name: str
    url: str

def git_fetch(repo: git.Repo, remote: str = "origin") -> str:
    origin = repo.remotes[remote]
    fetch_info = origin.fetch()
    if not fetch_info:
        return f"No updates from {remote}"
    return "\n".join(str(info) for info in fetch_info)

def git_pull(repo: git.Repo, remote: str = "origin", branch: str | None = None) -> str:
    try:
        origin = repo.remotes[remote]
        if branch:
            pull_info = origin.pull(branch)
        else:
            pull_info = origin.pull()
        if not pull_info:
            return f"Already up to date with {remote}"
        return "\n".join(str(info) for info in pull_info)
    except git.GitCommandError as e:
        if "There is no tracking information for the current branch" in str(e):
            return "No tracking information for current branch. Use --set-upstream to configure tracking."
        raise

def git_push(repo: git.Repo, remote: str = "origin", branch: str | None = None, set_upstream: bool = False) -> str:
    try:
        origin = repo.remotes[remote]
        if branch:
            if set_upstream:
                return repo.git.push('--set-upstream', remote, branch)
            return repo.git.push(remote, branch)
        return repo.git.push()
    except git.GitCommandError as e:
        if "no upstream branch" in str(e):
            return f"Current branch has no upstream branch. Use --set-upstream to configure tracking."
        raise

def git_remote_add(repo: git.Repo, name: str, url: str) -> str:
    repo.create_remote(name, url)
    return f"Added remote '{name}' with URL: {url}"