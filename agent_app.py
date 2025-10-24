#!/usr/bin/env python3
"""
Docker - GitHub Copilot Native Agent
A lightweight agent leveraging GitHub Copilot's native capabilities and VS Code Insiders
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

# Import configuration
from agent.config import CopilotAgentConfig

# Core dependencies only - no external AI services
try:
    import yaml  # type: ignore
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Local utilities
try:
    from docker_utils.config import load_config  # type: ignore
    from docker_utils.logging import setup_logging  # type: ignore
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Fallback configuration
    def load_config():
        return {
            'agent': {'name': 'docker-copilot-agent', 'debug': False},
            'server': {'host': '0.0.0.0', 'port': 8000},
            'logging': {'level': 'INFO'},
            'github': {'repo': 'docker_dotfiles', 'owner': 'DeanLuus22021994'}
        }

    def setup_logging(name: str, level: str = 'INFO'):
        logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
        return logging.getLogger(name)

# Configuration
config = load_config()
logger = setup_logging(__name__, level=config.get('logging', {}).get('level', 'INFO'))

class GitHubCopilotAgent:
    """GitHub Copilot Native Agent - No external AI dependencies"""

    def __init__(self, config: CopilotAgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{config.name}")
        self.tools: Dict[str, Callable] = {}
        self._github_available = self._check_github_cli()

        # Setup logging
        if config.__dict__.get('debug', False):
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        self.logger.info(f"Initializing GitHub Copilot Native Agent: {config.name}")

    def _check_github_cli(self) -> bool:
        """Check if GitHub CLI is available and authenticated"""
        try:
            # Set GH_TOKEN environment variable if GH_PAT is available
            gh_pat = os.getenv("GH_PAT")
            if gh_pat:
                os.environ["GH_TOKEN"] = gh_pat

            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    async def initialize(self):
        """Initialize the agent with GitHub Copilot native tools"""
        try:
            # Initialize tools
            await self._init_tools()

            # Validate GitHub integration
            if not self._github_available:
                self.logger.warning("GitHub CLI not available - some tools will be limited")

            self.logger.info("GitHub Copilot Native Agent initialized successfully")

        except Exception as e:
            self.logger.error("Failed to initialize agent", exc_info=True)
            raise

    async def _init_tools(self):
        """Initialize GitHub Copilot native tools"""
        tools_config = {
            "github_cli": self._create_github_cli_tool(),
            "file_operations": self._create_file_operations_tool(),
            "docker_operations": self._create_docker_operations_tool(),
            "config_management": self._create_config_management_tool(),
        }

        for tool_name in self.config.tools_enabled or []:
            if tool_name in tools_config:
                self.tools[tool_name] = tools_config[tool_name]
                self.logger.debug(f"Tool initialized: {tool_name}")

    def _create_github_cli_tool(self) -> Callable:
        """Create GitHub CLI tool for repository operations"""
        def github_cli(command: str, args: Optional[List[str]] = None) -> str:
            """Execute GitHub CLI commands"""
            if not self._github_available:
                return "GitHub CLI not available"

            try:
                cmd = ["gh"] + command.split() + (args or [])
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.config.workspace_root
                )

                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    return f"Error: {result.stderr.strip()}"

            except subprocess.TimeoutExpired:
                return "Command timed out"
            except Exception as e:
                return f"Exception: {str(e)}"

        return github_cli

    def _create_file_operations_tool(self) -> Callable:
        """Create file operations tool"""
        def file_operations(action: str, path: str, content: Optional[str] = None) -> str:
            """Perform file operations (read, write, list)"""
            try:
                full_path = Path(self.config.workspace_root) / path

                if action == "read":
                    if full_path.exists():
                        return full_path.read_text()
                    else:
                        return f"File not found: {path}"

                elif action == "write":
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content or "")
                    return f"File written: {path}"

                elif action == "list":
                    if full_path.is_dir():
                        return "\n".join(str(f) for f in full_path.iterdir())
                    else:
                        return f"Not a directory: {path}"

                else:
                    return f"Unknown action: {action}"

            except Exception as e:
                return f"File operation error: {str(e)}"

        return file_operations

    def _create_docker_operations_tool(self) -> Callable:
        """Create Docker operations tool"""
        def docker_operations(command: str, service: Optional[str] = None) -> str:
            """Execute Docker operations with automatic authentication"""
            try:
                # Auto-login to Docker Hub if credentials are available
                docker_username = os.getenv("DOCKER_USERNAME")
                docker_token = os.getenv("DOCKER_ACCESS_TOKEN")

                if docker_username and docker_token:
                    login_result = subprocess.run(
                        ["docker", "login", "-u", docker_username, "--password-stdin"],
                        input=docker_token,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if login_result.returncode != 0:
                        return f"Docker login failed: {login_result.stderr.strip()}"

                # Execute the requested Docker command
                if service:
                    cmd = ["docker-compose", command, service]
                else:
                    cmd = ["docker-compose"] + command.split()

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=self.config.workspace_root
                )

                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    return f"Docker error: {result.stderr.strip()}"

            except subprocess.TimeoutExpired:
                return "Docker command timed out"
            except FileNotFoundError:
                return "Docker Compose not found"
            except Exception as e:
                return f"Docker exception: {str(e)}"

        return docker_operations

    def _create_config_management_tool(self) -> Callable:
        """Create configuration management tool"""
        def config_management(action: str, config_type: str, data: Optional[Dict] = None) -> str:
            """Manage configuration files"""
            try:
                config_dir = Path(self.config.workspace_root) / ".config"

                if action == "read":
                    config_file = config_dir / config_type / "config.yml"
                    if config_file.exists():
                        if YAML_AVAILABLE:
                            with open(config_file) as f:
                                return yaml.safe_dump(yaml.safe_load(f))
                        else:
                            with open(config_file) as f:
                                return f.read()
                    else:
                        return f"Config not found: {config_type}"

                elif action == "write" and data:
                    config_file = config_dir / config_type / "config.yml"
                    config_file.parent.mkdir(parents=True, exist_ok=True)
                    if YAML_AVAILABLE:
                        with open(config_file, 'w') as f:
                            yaml.safe_dump(data, f)
                    else:
                        with open(config_file, 'w') as f:
                            f.write(str(data))
                    return f"Config written: {config_type}"

                elif action == "list":
                    if config_dir.exists():
                        return "\n".join(str(f.name) for f in config_dir.iterdir() if f.is_dir())
                    else:
                        return "Config directory not found"

                else:
                    return f"Unknown config action: {action}"

            except Exception as e:
                return f"Config management error: {str(e)}"

        return config_management

    async def run_task(self, task: str) -> Dict[str, Any]:
        """Run a task using GitHub Copilot native capabilities"""
        try:
            self.logger.info(f"Starting task: {task[:100]}...")

            # Parse task and determine which tools to use
            result = await self._execute_task(task)

            self.logger.info("Task completed successfully")
            return {
                "status": "success",
                "result": result,
                "agent": self.config.name,
                "tools_used": list(self.tools.keys())
            }

        except Exception as e:
            self.logger.error("Task failed", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "agent": self.config.name
            }

    async def _execute_task(self, task: str) -> str:
        """Execute task using available tools"""
        task_lower = task.lower()

        # Route tasks to appropriate tools
        if "github" in task_lower or "repo" in task_lower:
            github_tool = self.tools.get("github_cli")
            if github_tool:
                return github_tool("repo view")

        elif "file" in task_lower or "read" in task_lower or "write" in task_lower:
            file_tool = self.tools.get("file_operations")
            if file_tool:
                return file_tool("list", ".")

        elif "docker" in task_lower or "compose" in task_lower:
            docker_tool = self.tools.get("docker_operations")
            if docker_tool:
                return docker_tool("ps")

        elif "config" in task_lower:
            config_tool = self.tools.get("config_management")
            if config_tool:
                return config_tool("list")

        else:
            return f"Task executed via GitHub Copilot native agent: {task}"

        # Fallback if no tool matched
        return f"No suitable tool found for task: {task}"

    async def shutdown(self):
        """Shutdown the agent"""
        self.logger.info("GitHub Copilot Native Agent shutdown completed")

# FastAPI Application (minimal, no external dependencies)
try:
    from fastapi import FastAPI  # type: ignore
    from uvicorn import Config, Server  # type: ignore

    app = FastAPI(
        title="Docker GitHub Copilot Agent",
        description="Lightweight agent leveraging GitHub Copilot native capabilities",
        version="1.0.0"
    )

    # Global agent instance
    agent_instance: Optional[GitHubCopilotAgent] = None

    @app.on_event("startup")
    async def startup_event():
        """Initialize the agent on startup"""
        global agent_instance

        agent_config = CopilotAgentConfig(
            name=config.get('agent', {}).get('name', 'docker-copilot-agent'),
            workspace_root=config.get('workspace', {}).get('root', '/app'),
            github_repo=config.get('github', {}).get('repo', 'docker_dotfiles'),
            github_owner=config.get('github', {}).get('owner', 'DeanLuus22021994'),
        )

        agent_instance = GitHubCopilotAgent(agent_config)
        await agent_instance.initialize()

    @app.on_event("shutdown")
    async def shutdown_event():
        """Shutdown the agent on shutdown"""
        global agent_instance
        if agent_instance:
            await agent_instance.shutdown()

    @app.get("/")
    async def root():
        """Root endpoint"""
        return {"message": "Docker GitHub Copilot Agent API", "status": "running"}

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"status": "healthy", "agent": agent_instance.config.name if agent_instance else "not_initialized"}

    @app.post("/agent/run")
    async def run_agent(task: str):
        """Run the agent on a task"""
        if not agent_instance:
            return {"error": "Agent not initialized"}

        result = await agent_instance.run_task(task)
        return result

    @app.get("/agent/tools")
    async def get_agent_tools():
        """Get available agent tools"""
        if not agent_instance:
            return {"error": "Agent not initialized"}

        return {"tools": list(agent_instance.tools.keys())}

    if __name__ == "__main__":
        # Run the FastAPI application
        config_obj = Config(
            app=app,
            host=config.get('server', {}).get('host', '0.0.0.0'),
            port=config.get('server', {}).get('port', 8000),
            log_level="info"
        )

        server = Server(config_obj)
        asyncio.run(server.serve())  # type: ignore

except ImportError:
    # Fallback if FastAPI not available
    print("FastAPI not available - running in CLI mode only")

    async def main():
        agent_config = CopilotAgentConfig()
        agent = GitHubCopilotAgent(agent_config)
        await agent.initialize()

        # Example usage
        result = await agent.run_task("Check repository status")
        print(json.dumps(result, indent=2))

    if __name__ == "__main__":
        # Run the CLI mode agent - this is the entry point
        asyncio.run(main())  # type: ignore</content>
