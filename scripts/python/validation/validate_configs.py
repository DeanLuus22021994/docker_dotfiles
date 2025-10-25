#!/usr/bin/env python3
"""
Configuration Validation Script
Validates YAML, JSON, nginx, PostgreSQL, and MariaDB configs
Exit code: 0=success, 1=failure
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from python.utils.colors import error, header, separator, success


def validate_yaml_files() -> Tuple[bool, List[str]]:
    """Validate all YAML files with yamllint."""
    print(f"\n{header('=== Validating YAML Files ===')}")
    errors = []

    yaml_files = list(Path(".").rglob("*.yml")) + list(Path(".").rglob("*.yaml"))
    # Exclude node_modules and .git
    yaml_files = [f for f in yaml_files if ".git" not in str(f) and "node_modules" not in str(f)]

    if not yaml_files:
        print("No YAML files found")
        return True, []

    try:
        result = subprocess.run(
            [
                "yamllint",
                "-d",
                "{extends: default, rules: {line-length: {max: 120}, document-start: disable}}",
                ".",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            errors.append(f"yamllint failed:\n{result.stdout}")
            print(error("YAML validation failed"))
            print(result.stdout)
            return False, errors

        print(success(f"All {len(yaml_files)} YAML files valid"))
        return True, []

    except FileNotFoundError:
        errors.append("yamllint not found. Install with: pip install yamllint")
        print(error("yamllint not found"))
        return False, errors


def validate_json_files() -> Tuple[bool, List[str]]:
    """Validate all JSON files."""
    print(f"\n{header('=== Validating JSON Files ===')}")
    errors = []

    json_files = list(Path(".").rglob("*.json"))
    # Exclude node_modules, .git, and .vscode (JSONC files with comments)
    json_files = [
        f
        for f in json_files
        if ".git" not in str(f) and "node_modules" not in str(f) and ".vscode" not in str(f)
    ]

    if not json_files:
        print("No JSON files found")
        return True, []

    valid_count = 0
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                json.load(f)
            valid_count += 1
        except json.JSONDecodeError as e:
            errors.append(f"{json_file}: {e}")
            print(error(f"{json_file}: {e}"))

    if errors:
        print(error(f"{len(errors)} JSON file(s) invalid"))
        return False, errors

    print(success(f"All {valid_count} JSON files valid"))
    return True, []


def validate_nginx_configs() -> Tuple[bool, List[str]]:
    """Validate nginx configuration files."""
    print(f"\n{header('=== Validating nginx Configs ===')}")
    errors = []

    nginx_configs = [
        ".config/nginx/loadbalancer.conf",
        ".config/nginx/main.conf",
        ".config/nginx/default.conf",
    ]

    existing_configs = [f for f in nginx_configs if Path(f).exists()]

    if not existing_configs:
        print("No nginx configs found")
        return True, []

    for config in existing_configs:
        try:
            # Use docker to validate nginx config
            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-v",
                    f"{Path(config).absolute()}:/etc/nginx/test.conf:ro",
                    "nginx:alpine",
                    "nginx",
                    "-t",
                    "-c",
                    "/etc/nginx/test.conf",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                errors.append(f"{config}: nginx validation failed\n{result.stderr}")
                print(error(f"{config}: validation failed"))
                print(result.stderr)
            else:
                print(success(f"{config}: valid"))

        except FileNotFoundError:
            errors.append("Docker not found. Cannot validate nginx configs without Docker")
            print(error("Docker not found"))
            return False, errors

    if errors:
        print(error(f"{len(errors)} nginx config(s) invalid"))
        return False, errors

    print(success(f"All {len(existing_configs)} nginx configs valid"))
    return True, []


def validate_postgresql_config() -> Tuple[bool, List[str]]:
    """Validate PostgreSQL configuration."""
    print(f"\n{header('=== Validating PostgreSQL Config ===')}")
    errors = []

    pg_config = Path(".config/database/postgresql.conf")

    if not pg_config.exists():
        print("PostgreSQL config not found")
        return True, []

    # Basic syntax check - look for obvious issues
    try:
        with open(pg_config, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                errors.append(f"{pg_config}:{i}: Missing '=' in configuration line")
                print(error(f"{pg_config}:{i}: Missing '='"))

        if errors:
            print(error(f"PostgreSQL config has {len(errors)} error(s)"))
            return False, errors

        print(success("PostgreSQL config valid (basic syntax check)"))
        return True, []

    except Exception as e:
        errors.append(f"{pg_config}: {e}")
        print(error(f"{pg_config}: {e}"))
        return False, errors


def validate_mariadb_config() -> Tuple[bool, List[str]]:
    """Validate MariaDB configuration."""
    print(f"\n{header('=== Validating MariaDB Config ===')}")
    errors = []

    maria_config = Path(".config/database/mariadb.conf")

    if not maria_config.exists():
        print("MariaDB config not found")
        return True, []

    # Basic syntax check - look for obvious issues
    try:
        with open(maria_config, "r", encoding="utf-8") as f:
            lines = f.readlines()

        in_section = False
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                in_section = True
                continue

            if in_section and "=" not in line and "-" not in line:
                errors.append(f"{maria_config}:{i}: Invalid configuration line")
                print(error(f"{maria_config}:{i}: Invalid line"))

        if errors:
            print(error(f"MariaDB config has {len(errors)} error(s)"))
            return False, errors

        print(success("MariaDB config valid (basic syntax check)"))
        return True, []

    except Exception as e:
        errors.append(f"{maria_config}: {e}")
        print(error(f"{maria_config}: {e}"))
        return False, errors


def main() -> int:
    """Run all validation checks."""
    print(separator())
    print(header("Configuration Validation"))
    print(separator())

    all_errors: List[str] = []
    all_passed = True

    # Run all validations
    checks = [
        ("YAML", validate_yaml_files),
        ("JSON", validate_json_files),
        ("nginx", validate_nginx_configs),
        ("PostgreSQL", validate_postgresql_config),
        ("MariaDB", validate_mariadb_config),
    ]

    for _check_name, check_func in checks:
        passed, errors = check_func()
        if not passed:
            all_passed = False
            all_errors.extend(errors)

    # Final summary
    print(f"\n{separator()}")
    if all_passed:
        print(success("ALL VALIDATIONS PASSED"))
        print(separator())
        return 0
    else:
        print(error(f"VALIDATION FAILED ({len(all_errors)} error(s))"))
        print(separator())
        print("\nErrors:")
        for err in all_errors:
            print(f"  - {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
