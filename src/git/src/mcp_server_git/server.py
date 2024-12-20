import logging
from pathlib import Path
from typing import Sequence
from mcp.server import Server
from mcp.server.session import ServerSession
from mcp.server.stdio import stdio_server
from mcp.types import (
    ClientCapabilities,
    TextContent,
    Tool,
    ListRootsResult,
    RootsCapability,
)
from enum import Enum
import git

from .base import GitBaseModel
from .setup import GitInit, git_init
from .snapshot import (
    GitDiff, GitStatus, GitDiffUnstaged, GitDiffStaged, GitCommit, GitAdd, GitReset,
    git_diff, git_status, git_diff_unstaged, git_diff_staged, git_commit, git_add, git_reset
)
from .branch import (
    GitLog, GitCreateBranch, GitSwitch,
    git_log, git_create_branch, git_switch
)
from .sharing import (
    GitFetch, GitPull, GitPush, GitRemoteAdd,
    git_fetch, git_pull, git_push, git_remote_add
)

class GitTools(str, Enum):
    INIT = "git_init"
    DIFF = "git_diff"
    FETCH = "git_fetch"
    PULL = "git_pull"
    PUSH = "git_push"
    REMOTE_ADD = "git_remote_add"
    STATUS = "git_status"
    DIFF_UNSTAGED = "git_diff_unstaged"
    DIFF_STAGED = "git_diff_staged"
    COMMIT = "git_commit"
    ADD = "git_add"
    RESET = "git_reset"
    LOG = "git_log"
    CREATE_BRANCH = "git_create_branch"
    SWITCH = "git_switch"

async def serve(repository: Path | None) -> None:
    logger = logging.getLogger(__name__)

    if repository is not None:
        try:
            git.Repo(repository)
            logger.info(f"Using repository at {repository}")
        except git.InvalidGitRepositoryError:
            logger.error(f"{repository} is not a valid Git repository")
            return

    server = Server("mcp-git")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=GitTools.INIT,
                description="Initialize a new Git repository",
                inputSchema=GitInit.schema(),
            ),
            Tool(
                name=GitTools.DIFF,
                description="Show changes between current HEAD and another branch/commit/tag",
                inputSchema=GitDiff.schema(),
            ),
            Tool(
                name=GitTools.FETCH,
                description="Fetch refs and objects from another repository",
                inputSchema=GitFetch.schema(),
            ),
            Tool(
                name=GitTools.PULL,
                description="Fetch and integrate with another repository or branch",
                inputSchema=GitPull.schema(),
            ),
            Tool(
                name=GitTools.PUSH,
                description="Update remote refs along with associated objects",
                inputSchema=GitPush.schema(),
            ),
            Tool(
                name=GitTools.REMOTE_ADD,
                description="Add a new remote repository",
                inputSchema=GitRemoteAdd.schema(),
            ),
            Tool(
                name=GitTools.STATUS,
                description="Shows the working tree status",
                inputSchema=GitStatus.schema(),
            ),
            Tool(
                name=GitTools.DIFF_UNSTAGED,
                description="Shows changes in the working directory that are not yet staged",
                inputSchema=GitDiffUnstaged.schema(),
            ),
            Tool(
                name=GitTools.DIFF_STAGED,
                description="Shows changes that are staged for commit",
                inputSchema=GitDiffStaged.schema(),
            ),
            Tool(
                name=GitTools.COMMIT,
                description="Records changes to the repository",
                inputSchema=GitCommit.schema(),
            ),
            Tool(
                name=GitTools.ADD,
                description="Adds file contents to the staging area",
                inputSchema=GitAdd.schema(),
            ),
            Tool(
                name=GitTools.RESET,
                description="Unstages all staged changes",
                inputSchema=GitReset.schema(),
            ),
            Tool(
                name=GitTools.LOG,
                description="Shows the commit logs",
                inputSchema=GitLog.schema(),
            ),
            Tool(
                name=GitTools.CREATE_BRANCH,
                description="Creates a new branch from an optional base branch",
                inputSchema=GitCreateBranch.schema(),
            ),
            Tool(
                name=GitTools.SWITCH,
                description="Switch to another branch, optionally creating it with -c",
                inputSchema=GitSwitch.schema(),
            ),
        ]

    async def list_repos() -> Sequence[str]:
        async def by_roots() -> Sequence[str]:
            if not isinstance(server.request_context.session, ServerSession):
                raise TypeError("server.request_context.session must be a ServerSession")

            if not server.request_context.session.check_client_capability(
                ClientCapabilities(roots=RootsCapability())
            ):
                return []

            roots_result: ListRootsResult = await server.request_context.session.list_roots()
            logger.debug(f"Roots result: {roots_result}")
            repo_paths = []
            for root in roots_result.roots:
                path = root.uri.path
                try:
                    git.Repo(path)
                    repo_paths.append(str(path))
                except git.InvalidGitRepositoryError:
                    pass
            return repo_paths

        def by_commandline() -> Sequence[str]:
            return [str(repository)] if repository is not None else []

        cmd_repos = by_commandline()
        root_repos = await by_roots()
        return [*root_repos, *cmd_repos]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        repo_path = Path(arguments["repo_path"])
        
        # Special handling for git init since it doesn't require an existing repo
        if name == GitTools.INIT:
            result = git_init(repo_path)
            return [TextContent(
                type="text",
                text=result
            )]
        
        # For all other commands, we need an existing repo
        repo = git.Repo(repo_path)

        match name:
            case GitTools.DIFF:
                diff = git_diff(repo, arguments["other"])
                return [TextContent(
                    type="text",
                    text=diff
                )]

            case GitTools.FETCH:
                result = git_fetch(repo, arguments.get("remote", "origin"))
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.PULL:
                result = git_pull(
                    repo,
                    arguments.get("remote", "origin"),
                    arguments.get("branch")
                )
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.PUSH:
                result = git_push(
                    repo,
                    arguments.get("remote", "origin"),
                    arguments.get("branch"),
                    arguments.get("set_upstream", False)
                )
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.REMOTE_ADD:
                result = git_remote_add(repo, arguments["name"], arguments["url"])
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.STATUS:
                status = git_status(repo)
                return [TextContent(
                    type="text",
                    text=f"Repository status:\n{status}"
                )]

            case GitTools.DIFF_UNSTAGED:
                diff = git_diff_unstaged(repo)
                return [TextContent(
                    type="text",
                    text=f"Unstaged changes:\n{diff}"
                )]

            case GitTools.DIFF_STAGED:
                diff = git_diff_staged(repo)
                return [TextContent(
                    type="text",
                    text=f"Staged changes:\n{diff}"
                )]

            case GitTools.COMMIT:
                result = git_commit(repo, arguments["message"])
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.ADD:
                result = git_add(repo, arguments["files"])
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.RESET:
                result = git_reset(repo)
                return [TextContent(
                    type="text",
                    text=result
                )]

            case GitTools.LOG:
                log = git_log(repo, arguments.get("max_count", 10))
                return [TextContent(
                    type="text",
                    text="Commit history:\n" + "\n".join(log)
                )]

            case GitTools.CREATE_BRANCH:
                result = git_create_branch(
                    repo,
                    arguments["branch_name"],
                    arguments.get("base_branch")
                )
                return [TextContent(
                    type="text",
                    text=result
                )]
                
            case GitTools.SWITCH:
                result = git_switch(
                    repo,
                    arguments["branch_name"],
                    arguments.get("create_branch", False)
                )
                return [TextContent(
                    type="text",
                    text=result
                )]

            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)