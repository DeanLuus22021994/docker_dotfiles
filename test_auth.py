#!/usr/bin/env python3
"""
Simple test script for GitHub Copilot Agent authentication
"""

import os
import subprocess
import sys


def test_github_auth() -> bool:
    """Test GitHub CLI authentication"""
    print("🔍 Testing GitHub CLI authentication...")

    # Set GH_TOKEN from GH_PAT if available
    gh_pat = os.getenv("GH_PAT")
    if gh_pat:
        os.environ["GH_TOKEN"] = gh_pat
        print("✅ Set GH_TOKEN from GH_PAT")

    try:
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            print("✅ GitHub CLI authentication successful")
            print("GitHub auth status:")
            print(result.stdout)
            return True
        else:
            print("❌ GitHub CLI authentication failed")
            print("Error:", result.stderr)
            return False

    except FileNotFoundError:
        print("❌ GitHub CLI not found")
        return False
    except Exception as e:
        print(f"❌ GitHub CLI error: {e}")
        return False


def test_docker_auth() -> bool:
    """Test Docker Hub authentication"""
    print("\n🔍 Testing Docker authentication...")

    docker_username = os.getenv("DOCKER_USERNAME")
    docker_token = os.getenv("DOCKER_ACCESS_TOKEN")

    if not docker_username or not docker_token:
        print("❌ Docker credentials not found in environment")
        print(f"DOCKER_USERNAME: {'✅' if docker_username else '❌'}")
        print(f"DOCKER_ACCESS_TOKEN: {'✅' if docker_token else '❌'}")
        return False

    try:
        print(f"Logging in as {docker_username}...")
        result = subprocess.run(
            ["docker", "login", "-u", docker_username, "--password-stdin"],
            input=docker_token,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("✅ Docker authentication successful")
            return True
        else:
            print("❌ Docker authentication failed")
            print("Error:", result.stderr)
            return False

    except FileNotFoundError:
        print("❌ Docker not found")
        return False
    except Exception as e:
        print(f"❌ Docker error: {e}")
        return False


def test_repo_info() -> bool:
    """Test repository information"""
    print("\n🔍 Testing repository information...")

    try:
        result = subprocess.run(
            ["gh", "repo", "view"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            print("✅ Repository information retrieved")
            # Print first few lines
            lines = result.stdout.split("\n")[:5]
            for line in lines:
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            print("❌ Failed to get repository information")
            print("Error:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ Repository info error: {e}")
        return False


def main() -> None:
    """Main test function"""
    print("🚀 GitHub Copilot Agent Authentication Test")
    print("=" * 50)

    # Test GitHub authentication
    github_ok = test_github_auth()

    # Test Docker authentication
    docker_ok = test_docker_auth()

    # Test repository info if GitHub auth works
    if github_ok:
        repo_ok = test_repo_info()
    else:
        repo_ok = False

    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"GitHub Auth: {'✅' if github_ok else '❌'}")
    print(f"Docker Auth: {'✅' if docker_ok else '❌'}")
    print(f"Repo Info: {'✅' if repo_ok else '❌'}")

    if github_ok and docker_ok:
        print("\n🎉 All authentication tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
