# MCP (Model Context Protocol) Python Module

Python utilities for validating and analyzing MCP server configurations.

## Modules

### validate_config.py

Validates MCP configuration files against JSON schema and protocol requirements.

```python
from python.mcp import validate_mcp_config, MCPConfigValidator

# Quick validation
success, errors, warnings = validate_mcp_config(".vscode/mcp.json")

# Detailed validation
validator = MCPConfigValidator(Path(".vscode/mcp.json"))
success, errors, warnings = validator.validate()
```

**CLI Usage:**
```bash
# Validate default location
python scripts/python/mcp/validate_config.py

# Validate specific file
python scripts/python/mcp/validate_config.py .vscode/profiles/core.json

# Strict mode (warnings = errors)
python scripts/python/mcp/validate_config.py --strict
```

**Validates:**
- JSON syntax
- Required fields (servers, command, args)
- Valid commands (npx, uvx, node, python)
- Environment variable structure
- Metadata integrity (if present)

---

### analyze_tokens.py

Estimates token usage based on server and tool counts.

```python
from python.mcp import analyze_token_usage, TokenAnalyzer

# Quick analysis
stats = analyze_token_usage(".vscode/mcp.json")
print(f"Estimated tokens: {stats['estimated_tokens']}")

# Detailed analysis
analyzer = TokenAnalyzer(Path(".vscode/mcp.json"))
analyzer.load_config()
stats = analyzer.analyze()

# Compare profiles
comparison = analyzer.compare_profiles(Path(".vscode/profiles/core.json"))
```

**CLI Usage:**
```bash
# Analyze default config
python scripts/python/mcp/analyze_tokens.py

# Analyze specific file
python scripts/python/mcp/analyze_tokens.py .vscode/profiles/core.json

# Compare two configs
python scripts/python/mcp/analyze_tokens.py .vscode/mcp.json --compare .vscode/profiles/core.json

# JSON output
python scripts/python/mcp/analyze_tokens.py --json
```

**Calculates:**
- Tool count estimates (from known server tool counts)
- Token usage per tool (~180 tokens average)
- Server overhead (~50 tokens per server)
- Total estimated tokens
- Token range (±15% variance)

---

## Token Estimation Model

```
Total Tokens = (Tool Count × 180) + (Server Count × 50)

Where:
  180 tokens/tool = Average for name + description + input schema
  50 tokens/server = Server metadata and connection info
```

**Known Tool Counts:**
- playwright: 32 tools
- github: 26 tools
- filesystem: 14 tools
- git: 12 tools
- memory: 9 tools
- puppeteer: 7 tools
- sqlite: 5 tools
- postgres: 1 tool
- fetch: 1 tool

---

## Integration

Used by PowerShell orchestrator:

```powershell
# Validate config
python scripts/python/mcp/validate_config.py

# Analyze tokens
python scripts/python/mcp/analyze_tokens.py --json | ConvertFrom-Json
```

Used in CI/CD:

```bash
# Validate all profiles
for file in .vscode/configs/mcp/profiles/*.json; do
    python scripts/python/mcp/validate_config.py "$file" --strict || exit 1
done
```

---

## Requirements

- **Python:** 3.14+ (strict)
- **UV:** Preferred package manager
- **Dependencies:** None (uses stdlib only)

---

## Related Files

- **Profiles:** `.vscode/configs/mcp/profiles/`
- **Active Config:** `.vscode/mcp.json`
- **JavaScript Tools:** `scripts/javascript/mcp/`
- **PowerShell Tools:** `scripts/powershell/mcp/`

---

**Last Updated:** 2025-10-25
