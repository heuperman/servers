# mcp-server-git: A git MCP server

## Overview

A Model Context Protocol server for Git repository interaction and automation. This server provides tools to read, search, and manipulate Git repositories via Large Language Models.

Please note that mcp-server-git is currently in early development. The functionality and available tools are subject to change and expansion as we continue to develop and improve the server.

### Tools

1. `git_status`
   - Shows the working tree status
   - Input:
     - `repo_path` (string): Path to Git repository
   - Returns: Current status of working directory as text output

2. `git_diff_unstaged`
   - Shows changes in working directory not yet staged
   - Input:
     - `repo_path` (string): Path to Git repository
   - Returns: Diff output of unstaged changes

3. `git_diff_staged`
   - Shows changes that are staged for commit
   - Input:
     - `repo_path` (string): Path to Git repository
   - Returns: Diff output of staged changes

4. `git_commit`
   - Records changes to the repository
   - Inputs:
     - `repo_path` (string): Path to Git repository
     - `message` (string): Commit message
   - Returns: Confirmation with new commit hash

5. `git_add`
   - Adds file contents to the staging area
   - Inputs:
     - `repo_path` (string): Path to Git repository
     - `files` (string[]): Array of file paths to stage
   - Returns: Confirmation of staged files

6. `git_reset`
   - Unstages all staged changes
   - Input:
     - `repo_path` (string): Path to Git repository
   - Returns: Confirmation of reset operation

7. `git_log`
   - Shows the commit logs
   - Inputs:
     - `repo_path` (string): Path to Git repository
     - `max_count` (number, optional): Maximum number of commits to show (default: 10)
   - Returns: Array of commit entries with hash, author, date, and message

8. `git_create_branch`
   - Creates a new branch
   - Inputs:
     - `repo_path` (string): Path to Git repository
     - `branch_name` (string): Name of the new branch
     - `start_point` (string, optional): Starting point for the new branch
   - Returns: Confirmation of branch creation

9. `git_switch`
   - Switch to another branch
   - Inputs:
     - `repo_path` (string): Path to Git repository
     - `branch_name` (string): Name of the branch to switch to
     - `create_branch` (boolean, optional): Create new branch if it doesn't exist (-c flag)
   - Returns: Confirmation of branch switch operation

10. `git_init`
    - Initialize a new Git repository
    - Input:
      - `repo_path` (string): Path for the new repository
    - Returns: Confirmation of repository initialization

11. `git_diff`
    - Show changes between commits/branches
    - Inputs:
      - `repo_path` (string): Path to Git repository
      - `other` (string): Branch/commit/tag to compare against
    - Returns: Diff output of changes

12. `git_fetch`
    - Fetch refs and objects from another repository
    - Inputs:
      - `repo_path` (string): Path to Git repository
      - `remote` (string, optional): Remote to fetch from (default: "origin")
    - Returns: Fetch operation results

13. `git_pull`
    - Fetch and integrate with another repository or branch
    - Inputs:
      - `repo_path` (string): Path to Git repository
      - `remote` (string, optional): Remote to pull from (default: "origin")
      - `branch` (string, optional): Branch to pull
    - Returns: Pull operation results

14. `git_push`
    - Update remote refs along with objects
    - Inputs:
      - `repo_path` (string): Path to Git repository
      - `remote` (string, optional): Remote to push to (default: "origin")
      - `branch` (string, optional): Branch to push
      - `set_upstream` (boolean, optional): Set up tracking branch
    - Returns: Push operation results

15. `git_remote_add`
    - Add a new remote repository
    - Inputs:
      - `repo_path` (string): Path to Git repository
      - `name` (string): Name for the new remote
      - `url` (string): URL of the remote repository
    - Returns: Confirmation of remote addition

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-git*.

### Using PIP

Alternatively you can install `mcp-server-git` via pip:

```
pip install mcp-server-git
```

After installation, you can run it as a script using:

```
python -m mcp_server_git
```

## Configuration

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "git": {
    "command": "uvx",
    "args": ["mcp-server-git", "--repository", "path/to/git/repo"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "git": {
    "command": "python",
    "args": ["-m", "mcp_server_git", "--repository", "path/to/git/repo"]
  }
}
```
</details>

### Usage with [Zed](https://github.com/zed-industries/zed)

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "mcp-server-git": {
    "command": {
      "path": "uvx",
      "args": ["mcp-server-git"]
    }
  }
],
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "mcp-server-git": {
    "command": {
      "path": "python",
      "args": ["-m", "mcp_server_git"]
    }
  }
},
```
</details>

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```
npx @modelcontextprotocol/inspector uvx mcp-server-git
```

Or if you've installed the package in a specific directory or are developing on it:

```
cd path/to/servers/src/git
npx @modelcontextprotocol/inspector uv run mcp-server-git
```

Running `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` will show the logs from the server and may
help you debug any issues.

## Development

If you are doing local development, there are two ways to test your changes:

1. Run the MCP inspector to test your changes. See [Debugging](#debugging) for run instructions.

2. Test using the Claude desktop app. Add the following to your `claude_desktop_config.json`:

```json
"git": {
  "command": "uv",
  "args": [
    "--directory",
    "/<path to mcp-servers>/mcp-servers/src/git",
    "run",
    "mcp-server-git"
  ]
}
```

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.