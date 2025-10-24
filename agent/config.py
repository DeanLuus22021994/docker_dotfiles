"""
Configuration module for GitHub Copilot Agent
Contains all configuration dataclasses and settings
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CopilotAgentConfig:
    """GitHub Copilot native agent configuration"""
    name: str = "docker-copilot-agent"
    workspace_root: str = "/app"
    github_repo: str = "docker_dotfiles"
    github_owner: str = "DeanLuus22021994"
    mcp_enabled: bool = True
    vscode_extensions: Optional[List[str]] = None
    tools_enabled: Optional[List[str]] = None

    def __post_init__(self):
        if self.vscode_extensions is None:
            # Only use GitHub/Microsoft extensions with >10M downloads
            # Avoid deprecated extensions like GitHub Copilot Workspace
            self.vscode_extensions = [
                "ms-python.python",      # 100M+ downloads
                "ms-vscode.vscode-json", # 10M+ downloads
                "github.copilot",        # 50M+ downloads
                "github.copilot-chat"    # 20M+ downloads
            ]
        if self.tools_enabled is None:
            self.tools_enabled = [
                "github_cli",
                "file_operations",
                "docker_operations",
                "config_management"
            ]