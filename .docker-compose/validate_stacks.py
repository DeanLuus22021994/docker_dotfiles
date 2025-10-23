#!/usr/bin/env python3
"""
Docker Compose Examples Validation Script

Validates all docker-compose stacks for:
- Configuration syntax
- Build capabilities
- Service health checks
- Volume mount consistency
- Cross-stack compatibility

Usage:
    python validate_stacks.py [--build] [--test] [--cleanup]

Options:
    --build     Build all stack images
    --test      Run integration tests
    --cleanup   Clean up volumes and containers
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple


class StackValidator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.stacks = [
            "basic-stack",
            "cluster-example",
            "swarm-stack",
            "mcp/python_utils",
        ]

    def run_command(
        self, cmd: List[str], cwd: Optional[Path] = None, capture_output: bool = True
    ) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_path,
                capture_output=capture_output,
                text=True,
                timeout=300,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def validate_config(self, stack: str) -> bool:
        """Validate docker-compose configuration"""
        print(f"🔍 Validating {stack} configuration...")

        stack_path = self.base_path / stack
        if not stack_path.exists():
            print(f"❌ Stack directory not found: {stack_path}")
            return False

        compose_file = stack_path / "docker-compose.yml"
        if not compose_file.exists():
            print(f"❌ docker-compose.yml not found in {stack}")
            return False

        exit_code, stdout, stderr = self.run_command(
            ["docker-compose", "-f", str(compose_file), "config"], cwd=stack_path
        )

        if exit_code == 0:
            print(f"✅ {stack} configuration is valid")
            return True
        else:
            print(f"❌ {stack} configuration error: {stderr}")
            return False

    def build_stack(self, stack: str) -> bool:
        """Build docker images for a stack"""
        print(f"🏗️  Building {stack}...")

        stack_path = self.base_path / stack
        compose_file = stack_path / "docker-compose.yml"

        exit_code, stdout, stderr = self.run_command(
            ["docker-compose", "-f", str(compose_file), "build"], cwd=stack_path
        )

        if exit_code == 0:
            print(f"✅ {stack} built successfully")
            return True
        else:
            print(f"❌ {stack} build failed: {stderr}")
            return False

    def test_stack_health(self, stack: str) -> bool:
        """Test stack services health"""
        print(f"🏥 Testing {stack} health...")

        stack_path = self.base_path / stack
        compose_file = stack_path / "docker-compose.yml"

        # Start services
        exit_code, stdout, stderr = self.run_command(
            ["docker-compose", "-f", str(compose_file), "up", "-d"], cwd=stack_path
        )

        if exit_code != 0:
            print(f"❌ Failed to start {stack}: {stderr}")
            return False

        # Wait for services to be healthy
        time.sleep(30)

        # Check service status
        exit_code, stdout, stderr = self.run_command(
            ["docker-compose", "-f", str(compose_file), "ps"], cwd=stack_path
        )

        if exit_code != 0:
            print(f"❌ Failed to check {stack} status: {stderr}")
            return False

        # Parse status output for health
        healthy = True
        for line in stdout.split("\n"):
            if "Up" in line and (
                "healthy" in line.lower() or "running" in line.lower()
            ):
                continue
            elif "Up" in line:
                print(f"⚠️  Service may not be healthy: {line.strip()}")
            elif "Exit" in line or "unhealthy" in line.lower():
                print(f"❌ Unhealthy service: {line.strip()}")
                healthy = False

        if healthy:
            print(f"✅ {stack} services are healthy")
        else:
            print(f"❌ {stack} has unhealthy services")

        return healthy

    def cleanup_stack(self, stack: str) -> bool:
        """Clean up stack containers and volumes"""
        print(f"🧹 Cleaning up {stack}...")

        stack_path = self.base_path / stack
        compose_file = stack_path / "docker-compose.yml"

        exit_code, stdout, stderr = self.run_command(
            [
                "docker-compose",
                "-f",
                str(compose_file),
                "down",
                "-v",
                "--remove-orphans",
            ],
            cwd=stack_path,
        )

        if exit_code == 0:
            print(f"✅ {stack} cleaned up successfully")
            return True
        else:
            print(f"❌ {stack} cleanup failed: {stderr}")
            return False

    def validate_volume_consistency(self) -> bool:
        """Validate named volume consistency across stacks"""
        print("🔗 Validating volume consistency...")

        expected_volumes = {
            "react_scuba_python_venv",
            "python_cache",
            "python_pytest_cache",
            "python_mypy_cache",
            "python_ruff_cache",
            "node_modules",
            "node_cache",
            "node_yarn_cache",
            "db_data",
            "db_logs",
            "nginx_cache",
            "test_coverage",
        }

        found_volumes = set()

        for stack in self.stacks:
            stack_path = self.base_path / stack
            compose_file = stack_path / "docker-compose.yml"

            if not compose_file.exists():
                continue

            exit_code, stdout, stderr = self.run_command(
                ["docker-compose", "-f", str(compose_file), "config"], cwd=stack_path
            )

            if exit_code != 0:
                continue

            # Parse volumes from config output
            in_volumes_section = False
            for line in stdout.split("\n"):
                line = line.strip()
                if line.startswith("volumes:"):
                    in_volumes_section = True
                    continue
                elif in_volumes_section and line.startswith("networks:"):
                    break
                elif in_volumes_section and ":" in line and not line.startswith(" "):
                    volume_name = line.split(":")[0].strip()
                    found_volumes.add(volume_name)

        missing_volumes = expected_volumes - found_volumes
        extra_volumes = found_volumes - expected_volumes

        if missing_volumes:
            print(f"⚠️  Missing expected volumes: {missing_volumes}")

        if extra_volumes:
            print(f"ℹ️  Additional volumes found: {extra_volumes}")

        if not missing_volumes:
            print("✅ Volume consistency validated")
            return True
        else:
            print("❌ Volume consistency issues found")
            return False

    def run_validation(
        self, build: bool = False, test: bool = False, cleanup: bool = False
    ) -> bool:
        """Run complete validation suite"""
        print("🚀 Starting Docker Compose Examples Validation")
        print("=" * 50)

        results = []

        # Validate configurations
        print("\n📋 Phase 1: Configuration Validation")
        for stack in self.stacks:
            results.append(self.validate_config(stack))

        # Build stacks if requested
        if build:
            print("\n🏗️  Phase 2: Building Stacks")
            for stack in self.stacks:
                results.append(self.build_stack(stack))

        # Test health if requested
        if test:
            print("\n🏥 Phase 3: Health Testing")
            for stack in self.stacks:
                results.append(self.test_stack_health(stack))

        # Validate volume consistency
        print("\n🔗 Phase 4: Volume Consistency")
        results.append(self.validate_volume_consistency())

        # Cleanup if requested
        if cleanup:
            print("\n🧹 Phase 5: Cleanup")
            for stack in self.stacks:
                self.cleanup_stack(stack)

        # Summary
        print("\n📊 Validation Summary")
        print("=" * 50)

        passed = sum(results)
        total = len(results)

        print(f"Tests Passed: {passed}/{total}")

        if passed == total:
            print("🎉 All validations passed!")
            return True
        else:
            print("❌ Some validations failed")
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Docker Compose Examples")
    parser.add_argument("--build", action="store_true", help="Build all stack images")
    parser.add_argument("--test", action="store_true", help="Run integration tests")
    parser.add_argument(
        "--cleanup", action="store_true", help="Clean up volumes and containers"
    )

    args = parser.parse_args()

    base_path = Path(__file__).parent
    validator = StackValidator(base_path)

    success = validator.run_validation(
        build=args.build, test=args.test, cleanup=args.cleanup
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
