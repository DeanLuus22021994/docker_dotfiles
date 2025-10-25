# Bash Scripts

Bash automation scripts organized by task (SRP principle).

## Structure

```
bash/
├── docker/                  # Docker operations
│   └── start-devcontainer.sh  # Start development container
└── docs/                    # Documentation tasks
    └── serve-docs.sh        # Serve documentation server
```

## Usage

### Via Orchestrator (Recommended)

```bash
# Display help
../orchestrator.sh help

# Docker tasks
../orchestrator.sh docker start-devcontainer

# Documentation tasks
../orchestrator.sh docs serve

# Validation tasks (delegates to Python)
../orchestrator.sh validate env
../orchestrator.sh validate configs
```

### Direct Execution

```bash
# Docker
bash docker/start-devcontainer.sh
./docker/start-devcontainer.sh  # If executable

# Documentation
bash docs/serve-docs.sh
./docs/serve-docs.sh  # If executable
```

## Scripts Reference

### docker/start-devcontainer.sh
**Purpose:** Start Docker development container  
**Usage:** `bash docker/start-devcontainer.sh`  
**Exit Code:** 0 = success, 1 = error  
**Dependencies:** Docker, docker-compose

### docs/serve-docs.sh
**Purpose:** Serve Jekyll documentation server  
**Usage:** `bash docs/serve-docs.sh`  
**Exit Code:** 0 = success, 1 = error  
**Dependencies:** Docker, Jekyll image

## Common Patterns

### Script Header

All scripts use strict mode:

```bash
#!/usr/bin/env bash
#
# Script description
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures
```

### Color Output

Consistent color functions across scripts:

```bash
# Color output functions
success() { echo -e "\033[92m✓ $1\033[0m"; }
error() { echo -e "\033[91m✗ $1\033[0m" >&2; }
info() { echo -e "\033[94mℹ $1\033[0m"; }
warning() { echo -e "\033[93m⚠ $1\033[0m"; }
header() { echo -e "\033[1m\033[94m$1\033[0m"; }

# Usage
success "Operation completed"
error "Something went wrong"
warning "Please review this"
info "Processing..."
```

### Error Handling

```bash
# Function with error handling
do_something() {
    if ! command_that_might_fail; then
        error "Command failed"
        return 1
    fi
    success "Command succeeded"
    return 0
}

# Main execution
if ! do_something; then
    exit 1
fi
```

### Path Resolution

Use `SCRIPT_DIR` for relative paths:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/.config"
```

## Adding New Scripts

### 1. Create Script

```bash
#!/usr/bin/env bash
#
# Script description
# Usage: ./script-name.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color output functions
success() { echo -e "\033[92m✓ $1\033[0m"; }
error() { echo -e "\033[91m✗ $1\033[0m" >&2; }
info() { echo -e "\033[94mℹ $1\033[0m"; }

# Main logic
main() {
    info "Starting task..."
    
    # Do work
    if ! do_something; then
        error "Task failed"
        return 1
    fi
    
    success "Task completed"
    return 0
}

# Execute main
if ! main "$@"; then
    exit 1
fi
```

### 2. Make Executable

```bash
chmod +x category/script-name.sh
```

### 3. Add to Orchestrator

Update `../orchestrator.sh` switch statement:

```bash
case "$task" in
    category)
        case "$action" in
            action-name)
                script="${SCRIPT_DIR}/bash/category/script-name.sh"
                # Execute script
                ;;
        esac
        ;;
esac
```

### 4. Update README

Add to scripts reference table.

### 5. Test

```bash
# Direct execution
bash category/script-name.sh
./category/script-name.sh

# Via orchestrator
../orchestrator.sh category action-name
```

## Best Practices

### Naming Convention
- Use kebab-case: `start-devcontainer.sh`
- Action-oriented: `start-`, `serve-`, `deploy-`, `test-`
- One script per task (SRP)

### Error Messages
- Explicit: Show command, file paths
- Actionable: Provide fix command
- Colored: Use `error()`, `warning()` functions
- Write errors to stderr: `>&2`

### Variables
- Use UPPERCASE for environment variables: `$DOCKER_COMPOSE`
- Use lowercase for local variables: `$script_dir`
- Quote variables: `"$variable"` (prevents word splitting)
- Use `${variable}` for clarity

### Exit Codes
- `0` = Success
- `1` = Error
- `2` = Usage error
- Consistent across all scripts

### Functions
- One function per task
- Return codes for status (not echo)
- Error handling in each function

## Shell Compatibility

All scripts use **Bash 4.0+** features:

- Arrays: `files=(*.txt)`
- String manipulation: `${var//find/replace}`
- Process substitution: `<(command)`

If POSIX sh compatibility needed:
- Use `/bin/sh` instead of `/bin/bash`
- Avoid bash-specific features
- Test with `shellcheck --shell=sh`

## Linting

Use ShellCheck for validation:

```bash
# Install shellcheck
sudo apt install shellcheck  # Debian/Ubuntu
brew install shellcheck       # macOS

# Lint script
shellcheck script-name.sh

# Lint all bash scripts
find bash/ -name "*.sh" -exec shellcheck {} +
```

## Troubleshooting

### Permission Denied

Make script executable:

```bash
chmod +x script-name.sh
```

### Command Not Found

Ensure command is in PATH or use absolute path:

```bash
which docker
/usr/bin/docker --version
```

### Set -e Not Working

Use explicit error checking:

```bash
if ! command_that_might_fail; then
    error "Command failed"
    exit 1
fi
```

### Line Endings (Windows)

Convert CRLF to LF:

```bash
dos2unix script-name.sh
# Or:
sed -i 's/\r$//' script-name.sh
```

## Planned Scripts

- `docker/build-images.sh` - Build all Docker images
- `docker/cleanup-volumes.sh` - Clean up unused volumes
- `docs/build-docs.sh` - Build static documentation

---

**Last Updated:** 2025-10-25 (v3.0 refactor)
