---
date_created: '2025-10-27T02:37:41Z'
last_updated: '2025-10-27T02:37:41Z'
tags: [markdown, linting, markdownlint]
description: 'Markdown linting configuration'
---

# Markdownlint Configuration

Markdown style and consistency enforcement.

## 📁 Files

### `markdownlint.json`
**Markdownlint rules configuration**.

**Key Rules**:
- MD013: Line length (disabled - too restrictive)
- MD033: Inline HTML allowed (for documentation)
- MD041: First line must be H1 (enabled)

**Enabled Rules**: 40+ markdown linting rules

---

## 🚀 Quick Start

### Lint Markdown Files

```powershell
# Using pre-commit
pre-commit run markdownlint-cli2 --all-files

# Direct usage
markdownlint-cli2 \"**/*.md\"
```

---

## 📚 References

- [Markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
