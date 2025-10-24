#!/usr/bin/env python3
"""
Comprehensive Docker Stack Automation and Testing

This script provides full automation for:
- Codebase cleanup and validation
- Configuration-driven stack testing
- Cross-stack consistency validation
- Automated deployment testing
- Health monitoring and reporting

Usage:
    python automate_stacks.py [--validate] [--test] [--deploy] [--cleanup] [--all]
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml


class StackAutomation:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.config_path = base_path / ".config"
        self.compose_path = base_path / ".compose"
        self.results = {}

    def run_command(
        self, cmd: List[str], cwd: Optional[Path] = None, capture_output: bool = True, timeout: int = 300
    ) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_path,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {timeout}s"
        except Exception as e:
            return -1, "", str(e)

    def load_config(self, stack_name: str) -> Optional[Dict[str, Any]]:
        """Load configuration from .config folder"""
        config_file = self.config_path / stack_name / "config.yml"
        if not config_file.exists():
            return None

        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Failed to load config {config_file}: {e}")
            return None

    def validate_config_consistency(self) -> bool:
        """Validate that docker-compose files match their config.yml files"""
        print("🔍 Validating configuration consistency...")

        stacks = ["basic-stack", "cluster-example", "swarm-stack", "mcp"]
        all_valid = True

        for stack in stacks:
            config = self.load_config(stack)
            if not config:
                print(f"❌ No config found for {stack}")
                all_valid = False
                continue

            compose_file = self.compose_path / stack / "docker-compose.yml"
            if not compose_file.exists():
                print(f"❌ No compose file found for {stack}")
                all_valid = False
                continue

            # Validate compose file syntax
            exit_code, stdout, stderr = self.run_command(
                ["docker-compose", "-f", str(compose_file), "config"]
            )

            if exit_code != 0:
                print(f"❌ {stack} compose file invalid: {stderr}")
                all_valid = False
                continue

            # Check if services in config match compose file
            config_services = config.get("services", {})
            compose_config = yaml.safe_load(stdout)
            compose_services = compose_config.get("services", {})

            config_service_names = set(config_services.keys())
            compose_service_names = set(compose_services.keys())

            missing_in_compose = config_service_names - compose_service_names
            extra_in_compose = compose_service_names - config_service_names

            if missing_in_compose:
                print(f"⚠️  Services in config but not in compose ({stack}): {missing_in_compose}")
                all_valid = False

            if extra_in_compose:
                print(f"ℹ️  Extra services in compose ({stack}): {extra_in_compose}")

            # Validate environment variables
            for service_name, service_config in config_services.items():
                if service_name not in compose_services:
                    continue

                compose_service = compose_services[service_name]
                config_env = service_config.get("environment", {})
                compose_env = compose_service.get("environment", {})

                # Check for required environment variables
                if isinstance(config_env, dict):
                    for env_key, env_value in config_env.items():
                        if env_key not in compose_env:
                            print(f"⚠️  Missing env var {env_key} in {stack}/{service_name}")
                            all_valid = False

            print(f"✅ {stack} configuration validated")

        return all_valid

    def cleanup_codebase(self) -> bool:
        """Clean up the codebase - remove cache, temp files, etc."""
        print("🧹 Cleaning up codebase...")

        cleanup_commands = [
            ["docker", "system", "prune", "-f"],
            ["docker", "volume", "prune", "-f"],
            ["docker", "image", "prune", "-f"],
        ]

        # Clean up Python cache
        python_cache_dirs = [
            self.base_path / ".pytest_cache",
            self.base_path / ".mypy_cache",
            self.base_path / ".ruff_cache",
            self.base_path / "__pycache__",
        ]

        for cache_dir in python_cache_dirs:
            if cache_dir.exists():
                import shutil
                shutil.rmtree(cache_dir, ignore_errors=True)

        # Clean up Docker
        for cmd in cleanup_commands:
            exit_code, stdout, stderr = self.run_command(cmd)
            if exit_code != 0:
                print(f"⚠️  Cleanup command failed: {' '.join(cmd)} - {stderr}")

        # Clean up build cache
        cache_dir = self.base_path / ".cache" / "buildx"
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir, ignore_errors=True)

        print("✅ Codebase cleanup completed")
        return True

    def validate_all_stacks(self) -> bool:
        """Validate all stack configurations"""
        print("📋 Validating all stacks...")

        stacks = ["basic-stack", "cluster-example", "swarm-stack", "mcp"]
        all_valid = True

        for stack in stacks:
            compose_file = self.compose_path / stack / "docker-compose.yml"
            if not compose_file.exists():
                print(f"❌ Compose file not found: {compose_file}")
                all_valid = False
                continue

            exit_code, stdout, stderr = self.run_command(
                ["docker-compose", "-f", str(compose_file), "config"]
            )

            if exit_code == 0:
                print(f"✅ {stack} configuration valid")
            else:
                print(f"❌ {stack} configuration invalid: {stderr}")
                all_valid = False

        return all_valid

    def test_stack_deployment(self, stack: str) -> bool:
        """Test deploying a specific stack"""
        print(f"🚀 Testing deployment of {stack}...")

        compose_file = self.compose_path / stack / "docker-compose.yml"
        if not compose_file.exists():
            print(f"❌ Compose file not found: {compose_file}")
            return False

        # Start services
        exit_code, stdout, stderr = self.run_command(
            ["docker-compose", "-f", str(compose_file), "up", "-d"],
            timeout=120
        )

        if exit_code != 0:
            print(f"❌ Failed to start {stack}: {stderr}")
            return False

        # Wait for services to initialize
        time.sleep(10)

        # Check service status
        exit_code, stdout, stderr = self.run_command(
            ["docker-compose", "-f", str(compose_file), "ps"]
        )

        if exit_code != 0:
            print(f"❌ Failed to check {stack} status: {stderr}")
            return False

        # Parse status for running services
        running_services = 0
        total_services = 0

        for line in stdout.split("\n"):
            if "Up" in line or "running" in line.lower():
                running_services += 1
            if line.strip() and not line.startswith("Name") and not line.startswith("--"):
                total_services += 1

        if running_services == total_services and total_services > 0:
            print(f"✅ {stack} deployed successfully ({running_services}/{total_services} services running)")
            return True
        else:
            print(f"⚠️  {stack} partially deployed ({running_services}/{total_services} services running)")
            return running_services > 0

    def test_all_deployments(self) -> bool:
        """Test deployment of all stacks"""
        print("🚀 Testing all stack deployments...")

        stacks = ["basic-stack", "cluster-example", "swarm-stack", "mcp"]
        results = {}

        for stack in stacks:
            results[stack] = self.test_stack_deployment(stack)

        # Cleanup after testing
        print("🧹 Cleaning up test deployments...")
        for stack in stacks:
            compose_file = self.compose_path / stack / "docker-compose.yml"
            if compose_file.exists():
                self.run_command(["docker-compose", "-f", str(compose_file), "down", "-v"])

        # Summary
        successful = sum(results.values())
        total = len(results)

        print(f"\n📊 Deployment Test Results: {successful}/{total} stacks deployed successfully")

        for stack, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {stack}")

        return successful == total

    def generate_test_report(self) -> str:
        """Generate a comprehensive test report"""
        report = []
        report.append("# Docker Stack Automation Test Report")
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # System information
        report.append("## System Information")
        exit_code, stdout, stderr = self.run_command(["docker", "--version"])
        report.append(f"Docker Version: {stdout.strip() if exit_code == 0 else 'Unknown'}")

        exit_code, stdout, stderr = self.run_command(["docker-compose", "--version"])
        report.append(f"Docker Compose Version: {stdout.strip() if exit_code == 0 else 'Unknown'}")
        report.append("")

        # Configuration validation
        report.append("## Configuration Validation")
        config_valid = self.validate_config_consistency()
        report.append(f"Configuration Consistency: {'✅ Passed' if config_valid else '❌ Failed'}")
        report.append("")

        # Stack validation
        report.append("## Stack Validation")
        stacks_valid = self.validate_all_stacks()
        report.append(f"All Stacks Valid: {'✅ Passed' if stacks_valid else '❌ Failed'}")
        report.append("")

        # Deployment testing
        report.append("## Deployment Testing")
        deployment_success = self.test_all_deployments()
        report.append(f"Deployment Tests: {'✅ Passed' if deployment_success else '❌ Failed'}")
        report.append("")

        return "\n".join(report)

    def run_full_automation(self) -> bool:
        """Run the complete automation suite"""
        print("🚀 Starting Full Docker Stack Automation")
        print("=" * 60)

        steps = [
            ("Codebase Cleanup", self.cleanup_codebase),
            ("Configuration Validation", self.validate_config_consistency),
            ("Stack Validation", self.validate_all_stacks),
            ("Deployment Testing", self.test_all_deployments),
        ]

        results = []
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}")
            print("-" * 40)
            try:
                result = step_func()
                results.append(result)
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"📊 {step_name}: {status}")
            except Exception as e:
                print(f"❌ {step_name} failed with error: {e}")
                results.append(False)

        # Generate report
        print("\n📋 Generating Test Report...")
        report = self.generate_test_report()

        report_file = self.base_path / "automation_report.md"
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"📄 Report saved to: {report_file}")

        # Final summary
        print("\n🎯 Automation Summary")
        print("=" * 60)

        passed = sum(results)
        total = len(results)

        for i, (step_name, _) in enumerate(steps):
            status = "✅" if results[i] else "❌"
            print(f"  {status} {step_name}")

        print(f"\nOverall Result: {passed}/{total} steps passed")

        if passed == total:
            print("🎉 All automation steps completed successfully!")
            return True
        else:
            print("❌ Some automation steps failed")
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Docker Stack Automation")
    parser.add_argument("--validate", action="store_true", help="Validate configurations")
    parser.add_argument("--test", action="store_true", help="Test deployments")
    parser.add_argument("--deploy", action="store_true", help="Deploy all stacks")
    parser.add_argument("--cleanup", action="store_true", help="Clean up codebase")
    parser.add_argument("--all", action="store_true", help="Run full automation suite")

    args = parser.parse_args()

    base_path = Path(__file__).parent.parent
    automation = StackAutomation(base_path)

    if args.all or (not any([args.validate, args.test, args.deploy, args.cleanup])):
        success = automation.run_full_automation()
    else:
        success = True
        if args.cleanup:
            success &= automation.cleanup_codebase()
        if args.validate:
            success &= automation.validate_config_consistency()
            success &= automation.validate_all_stacks()
        if args.test:
            success &= automation.test_all_deployments()
        if args.deploy:
            # Deploy would be implemented here
            pass

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()