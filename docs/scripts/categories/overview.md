---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["scripts", "overview", "organization"]
description: "Scripts directory overview and organization"
---
# Scripts Overview

Organized scripts following SRP (Single Responsibility Principle) and DRY (Don't Repeat Yourself) principles.

## Structure

\\\
scripts/
├── orchestrator.{ps1,sh,py}  # Unified task execution
├── powershell/               # PowerShell scripts
├── python/                   # Python modules
└── bash/                     # Bash scripts
\\\

## Orchestrators

Unified interface across platforms:

\\\powershell
python scripts/orchestrator.py validate env
scripts/orchestrator.ps1 audit code
scripts/orchestrator.sh validate configs
\\\

## Available Categories

- **Validation** - Environment and config validation
- **Audit** - Code quality and dependency checks
- **Config** - Settings and secrets management
- **Docker** - Container operations
- **Docs** - Documentation serving

## Quick Start

\\\ash
# List all tasks
python scripts/orchestrator.py help

# Run validation
python scripts/orchestrator.py validate env

# Run code audit
python scripts/orchestrator.py audit code
\\\

See \categories/\ subdocs for language-specific details and \migration/\ for v3.0.0 changes.
