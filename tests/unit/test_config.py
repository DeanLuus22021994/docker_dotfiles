"""
Unit tests for GitHub Copilot Agent configuration
Following TDD principles: Red-Green-Refactor
"""

import pytest
from dataclasses import asdict
from agent.config import CopilotAgentConfig


class TestCopilotAgentConfig:
    """Test cases for CopilotAgentConfig dataclass"""

    def test_default_initialization(self):
        """Test default configuration values"""
        config = CopilotAgentConfig()

        assert config.name == "docker-copilot-agent"
        assert config.workspace_root == "/app"
        assert config.github_repo == "docker_dotfiles"
        assert config.github_owner == "DeanLuus22021994"
        assert config.mcp_enabled is True
        assert config.vscode_extensions is not None
        assert config.tools_enabled is not None

    def test_default_vscode_extensions(self):
        """Test that default VS Code extensions are properly set"""
        config = CopilotAgentConfig()

        expected_extensions = [
            "ms-python.python",      # 100M+ downloads
            "ms-vscode.vscode-json", # 10M+ downloads
            "github.copilot",        # 50M+ downloads
            "github.copilot-chat"    # 20M+ downloads
        ]

        assert config.vscode_extensions == expected_extensions

    def test_default_tools_enabled(self):
        """Test that default tools are properly enabled"""
        config = CopilotAgentConfig()

        expected_tools = [
            "github_cli",
            "file_operations",
            "docker_operations",
            "config_management"
        ]

        assert config.tools_enabled == expected_tools

    def test_custom_initialization(self):
        """Test custom configuration values"""
        custom_extensions = ["ms-vscode.vscode-typescript-next"]
        custom_tools = ["github_cli", "file_operations"]

        config = CopilotAgentConfig(
            name="custom-agent",
            workspace_root="/custom/workspace",
            github_repo="custom-repo",
            github_owner="custom-owner",
            mcp_enabled=False,
            vscode_extensions=custom_extensions,
            tools_enabled=custom_tools
        )

        assert config.name == "custom-agent"
        assert config.workspace_root == "/custom/workspace"
        assert config.github_repo == "custom-repo"
        assert config.github_owner == "custom-owner"
        assert config.mcp_enabled is False
        assert config.vscode_extensions == custom_extensions
        assert config.tools_enabled == custom_tools

    def test_asdict_conversion(self):
        """Test conversion to dictionary"""
        config = CopilotAgentConfig()
        config_dict = asdict(config)

        assert isinstance(config_dict, dict)
        assert config_dict["name"] == "docker-copilot-agent"
        assert config_dict["mcp_enabled"] is True
        assert "vscode_extensions" in config_dict
        assert "tools_enabled" in config_dict

    @pytest.mark.parametrize("field,value", [
        ("name", "test-agent"),
        ("workspace_root", "/test/path"),
        ("github_repo", "test-repo"),
        ("github_owner", "test-owner"),
        ("mcp_enabled", False),
    ])
    def test_field_assignment(self, field, value):
        """Test individual field assignments"""
        config = CopilotAgentConfig(**{field: value})
        assert getattr(config, field) == value