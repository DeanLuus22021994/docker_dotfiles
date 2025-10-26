#!/usr/bin/env python3
"""Python Orchestrator for Docker Infrastructure Scripts.

Central orchestrator for all Python-based automation scripts.
Delegates tasks to specialized scripts organized by function (SRP).
Uses Python 3.14 type system features for improved maintainability.

Usage:
    python orchestrator.py <task> <action>

Examples:
    python orchestrator.py validate env
    python orchestrator.py validate configs
    python orchestrator.py audit code
    python orchestrator.py mcp validate
"""

import subprocess
import sys
from pathlib import Path
from typing import Final, NoReturn, TypeAlias

# Type aliases
TaskName: TypeAlias = str
ActionName: TypeAlias = str
ScriptPath: TypeAlias = Path
ExitCode: TypeAlias = int

# Constants
SCRIPT_DIR: Final[Path] = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules
from python.utils.colors import error, header, info, success


def show_help() -> None:
    """Display help message"""
    print(f"\n{header('=== Python Orchestrator ===')}\n")
    print("Available Tasks:\n")

    print("validate")
    print("  env       Validate environment variables")
    print("  configs   Validate configuration files\n")

    print("audit")
    print("  code      Run code quality audit")
    print("  deps      Check dependencies and packages\n")

    print("mcp")
    print("  validate  Validate MCP configuration")
    print("  analyze   Analyze token usage\n")

    print("Examples:")
    print("  python orchestrator.py validate env")
    print("  python orchestrator.py mcp validate")
    print("  python orchestrator.py mcp analyze --json")
    print("  python orchestrator.py audit code\n")


def execute_task(task: TaskName, action: ActionName) -> NoReturn:
    """Execute specified task and action.

    Args:
        task: Task category (validate, audit, mcp, help)
        action: Specific action within task category

    Raises:
        SystemExit: Always exits with appropriate return code
    """

    if task == "validate":
        if action == "env":
            script = SCRIPT_DIR / "python" / "validation" / "validate_env.py"
            if script.exists():
                print(info("Validating environment variables..."))
                result = subprocess.run([sys.executable, str(script)], check=False)
                sys.exit(result.returncode)
            else:
                print(error(f"Script not found: {script}"))
                sys.exit(1)

        elif action == "configs":
            script = SCRIPT_DIR / "python" / "validation" / "validate_configs.py"
            if script.exists():
                print(info("Validating configuration files..."))
                result = subprocess.run([sys.executable, str(script)], check=False)
                sys.exit(result.returncode)
            else:
                print(error(f"Script not found: {script}"))
                sys.exit(1)

        else:
            print(error(f"Unknown validate action: {action}"))
            print(info("Available: env, configs"))
            sys.exit(1)

    elif task == "audit":
        if action == "code":
            script = SCRIPT_DIR / "python" / "audit" / "code_quality.py"
            if script.exists():
                print(info("Running code quality audit..."))
                result = subprocess.run([sys.executable, str(script)], check=False)
                sys.exit(result.returncode)
            else:
                print(error(f"Script not found: {script}"))
                sys.exit(1)

        elif action == "deps":
            script = SCRIPT_DIR / "python" / "audit" / "dependencies.py"
            if script.exists():
                print(info("Running dependencies audit..."))
                result = subprocess.run([sys.executable, str(script)], check=False)
                sys.exit(result.returncode)
            else:
                print(error(f"Script not found: {script}"))
                sys.exit(1)

        else:
            print(error(f"Unknown audit action: {action}"))
            print(info("Available: code, deps"))
            sys.exit(1)

    elif task == "mcp":
        if action == "validate":
            script = SCRIPT_DIR / "python" / "mcp" / "validate_config.py"
            if script.exists():
                print(info("Validating MCP configuration..."))
                result = subprocess.run([sys.executable, str(script)], check=False)
                sys.exit(result.returncode)
            else:
                print(error(f"Script not found: {script}"))
                sys.exit(1)

        elif action == "analyze":
            script = SCRIPT_DIR / "python" / "mcp" / "analyze_tokens.py"
            if script.exists():
                print(info("Analyzing MCP token usage..."))
                # Pass through any additional arguments
                extra_args = sys.argv[3:] if len(sys.argv) > 3 else []
                result = subprocess.run([sys.executable, str(script)] + extra_args, check=False)
                sys.exit(result.returncode)
            else:
                print(error(f"Script not found: {script}"))
                sys.exit(1)

        else:
            print(error(f"Unknown mcp action: {action}"))
            print(info("Available: validate, analyze"))
            sys.exit(1)

    elif task == "help":
        show_help()
        sys.exit(0)

    else:
        print(error(f"Unknown task: {task}"))
        show_help()
        sys.exit(1)


def main() -> None:
    """Main orchestrator entry point"""
    if len(sys.argv) < 3 or sys.argv[1] == "help":
        show_help()
        sys.exit(0)

    task = sys.argv[1]
    action = sys.argv[2]

    try:
        execute_task(task, action)
        # Note: execute_task calls sys.exit() with appropriate code
    except (OSError, subprocess.SubprocessError, KeyboardInterrupt) as e:
        print(error(f"Task failed: {type(e).__name__}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
