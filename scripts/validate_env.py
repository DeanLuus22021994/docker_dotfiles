#!/usr/bin/env python3
"""
Environment Variables Validation Script
Validates that all required environment variables are set before starting the stack.
"""

import os
import sys
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def validate_env_vars() -> Tuple[bool, List[str], List[str]]:
    """
    Validate required and optional environment variables.
    
    Returns:
        Tuple of (all_valid, missing_required, missing_optional)
    """
    # Required environment variables
    required_vars = {
        'GITHUB_OWNER': 'GitHub organization/username for API access',
        'GH_PAT': 'GitHub Personal Access Token for authentication',
        'DOCKER_POSTGRES_PASSWORD': 'PostgreSQL database password',
        'DOCKER_MARIADB_ROOT_PASSWORD': 'MariaDB root password',
        'DOCKER_MARIADB_PASSWORD': 'MariaDB cluster_user password',
        'DOCKER_REDIS_PASSWORD': 'Redis authentication password',
        'DOCKER_MINIO_ROOT_USER': 'MinIO root username',
        'DOCKER_MINIO_ROOT_PASSWORD': 'MinIO root password',
        'DOCKER_GRAFANA_ADMIN_PASSWORD': 'Grafana admin password',
        'DOCKER_JUPYTER_TOKEN': 'Jupyter notebook access token',
        'DOCKER_PGADMIN_PASSWORD': 'pgAdmin web interface password',
    }
    
    # Optional but recommended environment variables
    optional_vars = {
        'DOCKER_ACCESS_TOKEN': 'Docker Hub access token for increased pull limits',
        'CODECOV_TOKEN': 'Codecov token for coverage reporting',
    }
    
    missing_required = []
    missing_optional = []
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== Environment Variables Validation ==={Colors.RESET}\n")
    
    # Check required variables
    print(f"{Colors.BOLD}Required Variables:{Colors.RESET}")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"  {Colors.GREEN}✓{Colors.RESET} {var}: {masked_value}")
        else:
            print(f"  {Colors.RED}✗{Colors.RESET} {var}: NOT SET - {description}")
            missing_required.append(var)
    
    # Check optional variables
    print(f"\n{Colors.BOLD}Optional Variables:{Colors.RESET}")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"  {Colors.GREEN}✓{Colors.RESET} {var}: {masked_value}")
        else:
            print(f"  {Colors.YELLOW}⚠{Colors.RESET} {var}: NOT SET - {description}")
            missing_optional.append(var)
    
    all_valid = len(missing_required) == 0
    
    return all_valid, missing_required, missing_optional


def print_summary(all_valid: bool, missing_required: List[str], missing_optional: List[str]) -> None:
    """Print validation summary and instructions"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    
    if all_valid:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All required environment variables are set!{Colors.RESET}")
        
        if missing_optional:
            print(f"\n{Colors.YELLOW}⚠ Optional variables missing:{Colors.RESET}")
            for var in missing_optional:
                print(f"  - {var}")
            print(f"\n{Colors.YELLOW}Consider setting these for full functionality.{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}You can now start the stack:{Colors.RESET}")
        print(f"  docker-compose up -d")
        print(f"  docker-compose --profile dev up -d  # Include devcontainer")
        
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Missing required environment variables!{Colors.RESET}")
        print(f"\n{Colors.RED}Required variables missing:{Colors.RESET}")
        for var in missing_required:
            print(f"  - {var}")
        
        print(f"\n{Colors.BLUE}To fix this:{Colors.RESET}")
        print(f"  1. Copy .env.example to .env:")
        print(f"     cp .env.example .env")
        print(f"  2. Edit .env and fill in your values")
        print(f"  3. Source the .env file:")
        print(f"     export $(cat .env | xargs)  # Linux/macOS")
        print(f"     Get-Content .env | ForEach-Object {{ $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process') }}  # PowerShell")
        print(f"  4. Run this script again to verify")
    
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def main() -> int:
    """Main validation function"""
    all_valid, missing_required, missing_optional = validate_env_vars()
    print_summary(all_valid, missing_required, missing_optional)
    
    # Return exit code (0 = success, 1 = failure)
    return 0 if all_valid else 1


if __name__ == '__main__':
    sys.exit(main())
