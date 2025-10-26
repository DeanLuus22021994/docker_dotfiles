---
date_created: "2025-10-26T18:32:25.982879+00:00"
last_updated: "2025-10-26T18:32:25.982879+00:00"
tags: ['documentation', 'scripts', 'automation']
description: "Documentation for bash"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- scripts
description: Bash scripts organization and usage for Linux/macOS
---\n# Bash Scripts

## Categories

**`bash/docker/`** - Docker operations
- `start-devcontainer.sh` - Start development container (Linux/macOS)

**`bash/docs/`** - Documentation tools
- `serve-docs.sh` - Serve MkDocs documentation locally

## Usage

**Direct execution:**

```bash
bash scripts/bash/docker/start-devcontainer.sh
bash scripts/bash/docs/serve-docs.sh
```

**Via orchestrator:**

```bash
scripts/orchestrator.sh validate env
scripts/orchestrator.sh validate configs
```

## Requirements

- Bash 4.0+ (most Linux/macOS systems)
- Docker installed for docker scripts
- MkDocs for documentation scripts

## Permissions

Make scripts executable:

```bash
chmod +x scripts/bash/**/*.sh
```

## Shell Compatibility

Scripts use `#!/usr/bin/env bash` for portability. Compatible with:

- Ubuntu/Debian bash
- macOS bash (via Homebrew or built-in)
- WSL bash on Windows
- Most POSIX-compliant shells

See Bash README: `scripts/bash/README.md`
