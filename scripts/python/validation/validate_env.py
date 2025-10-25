#!/usr/bin/env python3
"""
Environment Variables Validation Script
Validates that all required environment variables are set before starting the stack.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
_script_dir = Path(__file__).parent.parent.parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from python.utils.colors import (
    Colors,
    bold,
    error,
    header,
    separator,
    success,
    warning,
)


def validate_env_vars() -> tuple[bool, list[str], list[str]]:
    """
    Validate required and optional environment variables.

    Returns:
        Tuple of (all_valid, missing_required, missing_optional)
    """
    # Required environment variables
    required_vars = {
        "GITHUB_OWNER": "GitHub organization/username for API access",
        "GH_PAT": "GitHub Personal Access Token for authentication",
        "DOCKER_POSTGRES_PASSWORD": "PostgreSQL database password",
        "DOCKER_MARIADB_ROOT_PASSWORD": "MariaDB root password",
        "DOCKER_MARIADB_PASSWORD": "MariaDB cluster_user password",
        "DOCKER_REDIS_PASSWORD": "Redis authentication password",
        "DOCKER_MINIO_ROOT_USER": "MinIO root username",
        "DOCKER_MINIO_ROOT_PASSWORD": "MinIO root password",
        "DOCKER_GRAFANA_ADMIN_PASSWORD": "Grafana admin password",
        "DOCKER_JUPYTER_TOKEN": "Jupyter notebook access token",
        "DOCKER_PGADMIN_PASSWORD": "pgAdmin web interface password",
    }

    # Optional but recommended environment variables
    optional_vars = {
        "DOCKER_ACCESS_TOKEN": "Docker Hub access token for increased pull limits",
        "CODECOV_TOKEN": "Codecov token for coverage reporting",
    }

    missing_required: list[str] = []
    missing_optional: list[str] = []

    print(f"\n{header('=== Environment Variables Validation ===')}\n")

    # Check required variables
    print(f"{bold('Required Variables:')}")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"  {success(f'{var}: {masked_value}')}")
        else:
            print(f"  {error(f'{var}: NOT SET - {description}')}")
            missing_required.append(var)

    # Check optional variables
    print(f"\n{bold('Optional Variables:')}")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"  {success(f'{var}: {masked_value}')}")
        else:
            print(f"  {warning(f'{var}: NOT SET - {description}')}")
            missing_optional.append(var)

    all_valid = len(missing_required) == 0

    return all_valid, missing_required, missing_optional


def print_summary(
    all_valid: bool, missing_required: list[str], missing_optional: list[str]
) -> None:
    """Print validation summary and instructions"""
    print(f"\n{separator()}")

    if all_valid:
        print(f"{success('All required environment variables are set!')}")

        if missing_optional:
            print(f"\n{warning('Optional variables missing:')}")
            for var in missing_optional:
                print(f"  - {var}")
            print(f"\n{warning('Consider setting these for full functionality.')}")

        print(f"\n{Colors.GREEN}You can now start the stack:{Colors.RESET}")
        print("  docker-compose up -d")
        print("  docker-compose --profile dev up -d  # Include devcontainer")

    else:
        print(f"{error('Missing required environment variables!')}")
        print(f"\n{Colors.RED}Required variables missing:{Colors.RESET}")
        for var in missing_required:
            print(f"  - {var}")

        print(f"\n{Colors.BLUE}To fix this:{Colors.RESET}")
        print("  1. Copy .env.example to .env:")
        print("     cp .env.example .env")
        print("  2. Edit .env and fill in your values")
        print("  3. Source the .env file:")
        print("     export $(cat .env | xargs)  # Linux/macOS")
        powershell_cmd = (
            "     Get-Content .env | ForEach-Object { $var = $_.Split('='); "
            "[Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process') }  # PowerShell"
        )
        print(powershell_cmd)
        print("  4. Run this script again to verify")

    print(f"{separator()}\n")


def main() -> int:
    """Main validation function"""
    all_valid, missing_required, missing_optional = validate_env_vars()
    print_summary(all_valid, missing_required, missing_optional)

    # Return exit code (0 = success, 1 = failure)
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
