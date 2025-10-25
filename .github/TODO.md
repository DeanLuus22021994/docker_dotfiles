---
title: "Docker Infrastructure Refactoring - TODO"
version: "3.0.0"
date: "2025-10-25"
status: "IN_PROGRESS"
previous_version: "2.0.0"
archived_date: "2025-10-25"
iteration: 3
---

# Docker Infrastructure Refactoring - TODO v3.0

## 🎯 Overview

This iteration focuses on **codebase cleanup, Python environment resolution, and scripts reorganization** following SRP (Single Responsibility Principle) and DRY (Don't Repeat Yourself) principles.

**Critical Issue:** Python not found on host system - blocking all validation workflows and scripts.

**Goal:** Clean, maintainable, organized scripts architecture with proper Python environment setup.

---

## 📋 Phase 1: Codebase Cleanup & Maintenance ⏳ IN PROGRESS

**Objective:** Ensure absolutely clean code implementations before new features.

### Task 1.1: Code Quality Audit ✅ COMPLETE
- [x] Run semantic search for code smells, duplications, and inconsistencies
- [x] Identify unused files, deprecated code, and orphaned configurations
- [x] Document findings in `CLEANUP-REPORT.md`
- [x] Create removal plan for obsolete code

**Acceptance Criteria:**
- ✅ Comprehensive audit report generated
- ✅ Zero duplicate configuration blocks identified  
- ✅ All orphaned files documented
- ✅ Removal plan approved

**Commit:** `6d2f25f`

---

### Task 1.2: Remove Deprecated Code
- [ ] Delete archived documentation (already excluded from Jekyll)
- [ ] Remove unused Docker images/services
- [ ] Clean up obsolete scripts (if any identified in audit)
- [ ] Remove commented-out code blocks

**Files to Review:**
- `documentation/archive/` - Already excluded, verify removal
- ~~`ENHANCEMENTS-COMPLETE.md`~~ - Does not exist (references removed)
- ~~`ENVIRONMENT-INTEGRATION-COMPLETE.md`~~ - Does not exist (references removed)
- ~~`CLUSTER.md`~~ - Does not exist (references removed)

---

### Task 1.3: Standardize Code Formatting
- [ ] Run Black on all Python files
- [ ] Run Ruff linter and fix issues
- [ ] Run mypy type checking (strict mode)
- [ ] Ensure pre-commit hooks pass on all files

---

### Task 1.4: Documentation Cleanup
- [ ] Remove outdated sections from README.md
- [ ] Update AGENT.md with new scripts structure
- [ ] Consolidate scattered documentation into centralized locations
- [ ] Ensure all code blocks have correct language identifiers

---

## 🐍 Phase 2: Python Environment Resolution (CRITICAL)

**Objective:** Resolve "Python was not found" error on Windows host.

### Task 2.1: Diagnose Python Installation
- [ ] Document current Python installations on host
- [ ] Identify PATH issues
- [ ] Check Windows App Execution Aliases
- [ ] Determine if using Python from Microsoft Store (problematic)

---

### Task 2.2: Install Python 3.13 (Standalone)
- [ ] Download Python 3.13 from python.org (NOT Microsoft Store)
- [ ] Install for all users OR current user (document choice)
- [ ] Add Python to PATH during installation
- [ ] Disable Windows App Execution Aliases for Python

---

### Task 2.3: Configure Python for Scripts
- [ ] Update pyproject.toml if needed
- [ ] Install Python dependencies via UV
- [ ] Test all validation scripts
- [ ] Update GitHub Actions if Python version changed

---

### Task 2.4: Update Documentation
- [ ] Add Python setup instructions to README.md
- [ ] Create troubleshooting guide for Python issues
- [ ] Update SETUP.md with Python prerequisites
- [ ] Document UV vs pip usage

---

## 📁 Phase 3: Scripts Reorganization (SRP & DRY)

**Objective:** Organize scripts into language-specific folders with task-based structure.

### Task 3.1: Design New Scripts Structure
**Proposed Structure:**
```
scripts/
├── README.md
├── orchestrator.ps1
├── orchestrator.sh
├── orchestrator.py
├── powershell/
│   ├── config/
│   ├── docker/
│   ├── docs/
│   ├── audit/
│   └── cleanup/
├── python/
│   ├── validation/
│   ├── audit/
│   └── utils/
└── bash/
    ├── docker/
    └── docs/
```

---

### Task 3.2: Create Orchestrator Scripts
- [ ] `scripts/orchestrator.ps1`
- [ ] `scripts/orchestrator.sh`
- [ ] `scripts/orchestrator.py`

---

### Task 3.3: Migrate Existing Scripts
- [ ] Move PowerShell scripts to `powershell/` subfolders
- [ ] Move Python scripts to `python/` subfolders
- [ ] Move Bash scripts to `bash/` subfolders
- [ ] Update all references

---

### Task 3.4: Extract Shared Utilities (DRY)
- [ ] Create `python/utils/colors.py`
- [ ] Create `python/utils/file_utils.py`
- [ ] Create `python/utils/logging_utils.py`
- [ ] Update all Python scripts to import shared utilities

---

### Task 3.5: Update References
- [ ] Update `.github/workflows/validate.yml`
- [ ] Update `.github/workflows/ci.yml`
- [ ] Update `Makefile`
- [ ] Update documentation

---

### Task 3.6: Create Scripts Documentation
- [ ] Create `scripts/README.md`
- [ ] Create `scripts/powershell/README.md`
- [ ] Create `scripts/python/README.md`
- [ ] Create `scripts/bash/README.md`

---

## 🧪 Phase 4: Testing & Validation

### Task 4.1: Test Python Scripts
### Task 4.2: Test PowerShell Scripts
### Task 4.3: Test Bash Scripts
### Task 4.4: Integration Testing

---

## 📊 Phase 5: Documentation Updates

### Task 5.1: Update Core Documentation
### Task 5.2: Create New Documentation
### Task 5.3: Update Workflow Documentation

---

## ✅ Acceptance Criteria (All Phases)

### Phase 1: Cleanup
- ✅ Zero code smells (Ruff clean)
- ✅ 100% Black formatting compliance
- ✅ Mypy strict mode passes
- ✅ Pre-commit hooks green
- ✅ All obsolete files archived/removed

### Phase 2: Python
- ✅ Python 3.13 installed and in PATH
- ✅ UV package manager installed
- ✅ All Python scripts run without errors

### Phase 3: Scripts
- ✅ Scripts organized by language and task
- ✅ Orchestrators working
- ✅ Shared utilities extracted (DRY)
- ✅ Each script follows SRP

### Phase 4: Testing
- ✅ All scripts tested individually
- ✅ GitHub Actions workflows pass

### Phase 5: Documentation
- ✅ All documentation updated
- ✅ New docs created

---

## 📝 Critical Issue Resolution

**Problem:** `Python was not found; run without arguments to install from the Microsoft Store`

**Root Cause:** Windows App Execution Aliases redirect `python` to Microsoft Store.

**Solution:** Phase 2 (Tasks 2.1 - 2.4)

---

## 📅 Timeline Estimate

- **Phase 1: Cleanup** - 2-3 hours
- **Phase 2: Python** - 1-2 hours
- **Phase 3: Scripts** - 4-6 hours
- **Phase 4: Testing** - 2-3 hours
- **Phase 5: Documentation** - 2-3 hours

**Total:** 11-17 hours over 2-3 days

---

## 🔄 Migration Tracking

| Old Path | New Path | Status |
|----------|----------|--------|
| `scripts/apply-settings.ps1` | `scripts/powershell/config/apply-settings.ps1` | ⏳ Pending |
| `scripts/setup_secrets.ps1` | `scripts/powershell/config/setup-secrets.ps1` | ⏳ Pending |
| `scripts/validate_env.py` | `scripts/python/validation/validate_env.py` | ⏳ Pending |
| `scripts/validate_configs.py` | `scripts/python/validation/validate_configs.py` | ⏳ Pending |

---

## ✍️ Changelog

### v3.0.0 (2025-10-25)
- Initial planning for codebase cleanup and scripts reorganization
- Identified critical Python installation issue
- Designed new scripts structure (SRP, DRY principles)
- Created orchestrator pattern

---

**Status:** 🟢 IN PROGRESS - Phase 1 Task 1.1
**Next Action:** Run codebase audit using semantic search
