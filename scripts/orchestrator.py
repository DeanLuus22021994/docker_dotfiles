#!/usr/bin/env python3
"""
Python Orchestrator for Docker Infrastructure Scripts
Central orchestrator for all Python-based automation scripts
Delegates tasks to specialized scripts organized by function (SRP)

Usage:
    python orchestrator.py <task> <action>

Examples:
    python orchestrator.py validate env
    python orchestrator.py validate configs
"""

import subprocess
import sys
from pathlib import Path

# Add scripts directory to path before other imports
SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules
from python.utils.colors import error, header, info, success, warning


def show_help() -> None:
    """Display help message"""
    print(f"\n{header('=== Python Orchestrator ===')}\n")
    print("Available Tasks:\n")

    print("validate")
    print("  env       Validate environment variables")
    print("  configs   Validate configuration files\n")

    print("audit")
    print("  code      Run code quality audit\n")

    print("Examples:")
    print("  python orchestrator.py validate env")
    print("  python orchestrator.py validate configs")
    print("  python orchestrator.py audit code\n")


def execute_task(task: str, action: str) -> None:
    """Execute specified task and action"""

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
            print(info("Code quality audit not yet implemented"))
            print(warning("Refer to CLEANUP-REPORT.md for manual audit results"))
            sys.exit(0)
        else:
            print(error(f"Unknown audit action: {action}"))
            print(info("Available: code"))
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
        print(success(f"Task completed: {task} {action}"))
    except (OSError, subprocess.SubprocessError, KeyboardInterrupt) as e:
        print(error(f"Task failed: {type(e).__name__}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
