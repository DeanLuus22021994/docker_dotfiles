# MCP Profile Testing Guide

## Overview

Comprehensive testing ensures MCP profiles are generated correctly with GitHub and Filesystem servers always positioned first.

## Quick Test

```powershell
# Run all tests
.\scripts\orchestrator.ps1 mcp test-profiles

# Clean test from scratch
.\scripts\powershell\mcp\Test-McpProfileGeneration.ps1 -CleanTest
```

## Test Coverage

### 1. Directory Structure (1 test)
- ✓ Profiles directory exists

### 2. Profile Generation (1 test)
- ✓ Profile generation command executes

### 3. File Existence (4 tests)
- ✓ core.json exists
- ✓ fullstack.json exists
- ✓ testing.json exists
- ✓ data.json exists

### 4. JSON Structure & Server Order (40 tests)

**Per Profile (10 tests each):**
- ✓ Has servers object
- ✓ GitHub is first server
- ✓ Filesystem is second server
- ✓ Has _metadata object
- ✓ Metadata has profile_name
- ✓ Metadata has tool_count
- ✓ Metadata has estimated_tokens
- ✓ Metadata has last_generated
- ✓ Metadata has servers_enabled
- ✓ Metadata servers_enabled has github, filesystem first

### 5. Profile Switching & mcp.json Creation (5 tests)
- ✓ mcp.json created after switch
- ✓ Active mcp.json has github first
- ✓ Active mcp.json has filesystem second
- ✓ Active mcp.json matches profile
- ✓ Backup restoration works

### 6. All Profile Switches (4 tests)
- ✓ core switch creates mcp.json with correct order
- ✓ fullstack switch creates mcp.json with correct order
- ✓ testing switch creates mcp.json with correct order
- ✓ data switch creates mcp.json with correct order

### 7. Python Validation (4 tests)
- ✓ core.json passes Python validation
- ✓ fullstack.json passes Python validation
- ✓ testing.json passes Python validation
- ✓ data.json passes Python validation

### 8. Token Analysis (4 tests)
- ✓ core token analysis successful (Est: 9740 tokens)
- ✓ fullstack token analysis successful (Est: 14800 tokens)
- ✓ testing token analysis successful (Est: 15960 tokens)
- ✓ data token analysis successful (Est: 8810 tokens)

## Total: 62 Tests

## Expected Results

```
Total Tests: 62
Passed: 62
Failed: 0
Pass Rate: 100%

✓ ALL TESTS PASSED!
```

## What's Validated

### Server Order
Every profile guarantees:
1. **github** is always the first server
2. **filesystem** is always the second server
3. Remaining servers follow in profile-specific order

### JSON Structure
```json
{
  "servers": {
    "github": { ... },
    "filesystem": { ... },
    ...
  },
  "_metadata": {
    "profile_name": "core",
    "tool_count": 53,
    "estimated_tokens": "8-10k",
    "last_generated": "2025-10-25T21:50:00Z",
    "servers_enabled": ["github", "filesystem", "git", "fetch"]
  }
}
```

### Profile Switching
1. Reads profile from `.vscode/configs/mcp/profiles/<name>.json`
2. Creates backup of current `.vscode/mcp.json`
3. Copies profile to `.vscode/mcp.json`
4. Validates server order maintained
5. Requires VS Code restart to apply

## Integration Testing

### Python Validation
```bash
python scripts/python/mcp/validate_config.py .vscode/configs/mcp/profiles/core.json
```

**Checks:**
- JSON syntax
- Required fields (servers, command, args)
- Valid commands (npx, uvx, node, python)
- Environment variable structure
- Metadata integrity

### Token Analysis
```bash
python scripts/python/mcp/analyze_tokens.py .vscode/configs/mcp/profiles/core.json
```

**Estimates:**
- Tool count (from known server tool counts)
- Token usage (180 tokens/tool + 50 tokens/server)
- Token range (±15% variance)

## CI/CD Integration

```yaml
# .github/workflows/test-mcp.yml
name: Test MCP Profiles

on: [push, pull_request]

jobs:
  test-profiles:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      
      - name: Test MCP Profiles
        run: .\scripts\orchestrator.ps1 mcp test-profiles
```

## Troubleshooting

### Test Failures

**Profile not found:**
```powershell
# Regenerate profiles
.\scripts\orchestrator.ps1 mcp new-profiles
```

**Server order incorrect:**
```powershell
# Clean regeneration
.\scripts\powershell\mcp\Test-McpProfileGeneration.ps1 -CleanTest
```

**Python validation fails:**
```bash
# Check Python environment
python --version  # Should be 3.14
python scripts/python/mcp/validate_config.py .vscode/mcp.json
```

**Token analysis fails:**
```bash
# Verify module imports
python -c "from scripts.python.utils.colors import Colors"
```

## Manual Verification

```powershell
# 1. Generate profiles
.\scripts\orchestrator.ps1 mcp new-profiles

# 2. Check core.json server order
$core = Get-Content .vscode\configs\mcp\profiles\core.json | ConvertFrom-Json
$core.servers.PSObject.Properties.Name[0..1]  # Should be: github, filesystem

# 3. Switch profile and verify mcp.json
.\scripts\orchestrator.ps1 mcp set-profile -Profile core
$mcp = Get-Content .vscode\mcp.json | ConvertFrom-Json
$mcp.servers.PSObject.Properties.Name[0..1]  # Should be: github, filesystem

# 4. Validate with Python
python scripts\python\mcp\validate_config.py .vscode\mcp.json

# 5. Analyze tokens
python scripts\python\mcp\analyze_tokens.py .vscode\mcp.json --json
```

## Continuous Verification

```powershell
# Run before commits
.\scripts\orchestrator.ps1 mcp test-profiles

# Quick validation
python scripts\python\mcp\validate_config.py .vscode\mcp.json

# Token check
python scripts\python\mcp\analyze_tokens.py .vscode\mcp.json
```

---

**Last Updated:** 2025-10-25  
**Test Suite Version:** 1.0.0  
**Total Tests:** 62  
**Coverage:** Profile generation, structure, switching, validation, analysis
