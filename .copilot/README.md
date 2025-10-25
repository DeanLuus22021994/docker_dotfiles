# GitHub Copilot Configuration

This directory contains configuration files to optimize GitHub Copilot Chat performance for this repository.

## Files

### `ignore`
Defines patterns for files and directories that should be excluded from Copilot's context. This significantly improves performance by:
- Reducing the amount of data Copilot needs to process
- Excluding irrelevant files (build artifacts, caches, node_modules)
- Focusing on actual source code

**Impact**: Can reduce context size by 60-80%, improving response latency

### `instructions.md`
Provides context-specific guidance to Copilot about:
- Project structure and technology stack
- Coding standards and best practices
- Common commands and workflows
- Important files and their purposes

**Impact**: Improves response accuracy and relevance

## How It Works

1. **`.copilot/ignore`**: GitHub Copilot reads this file to determine which files to exclude from indexing
2. **`.copilot/instructions.md`**: Provides project-specific context to improve suggestions
3. **`.copilotignore`** (root): Fallback ignore file, defers to `.copilot/ignore`

## Performance Benefits

With this configuration:
- ✅ Faster response times (less data to process)
- ✅ More relevant suggestions (focused on source code)
- ✅ Better context awareness (project-specific instructions)
- ✅ Reduced token usage (excludes large/irrelevant files)

## Maintenance

Update these files when:
- Adding new large directories that should be excluded
- Changing project structure significantly
- Adding new coding standards or conventions
- New developers need onboarding information

## Related Files

- `.github/copilot-instructions.md` - Main Copilot instructions
- `.github/instructions/agent.instructions.md` - Agent-specific rules
- `.copilotignore` - Root-level ignore file (defers to this directory)

## References

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Copilot Ignore Files](https://docs.github.com/en/copilot/configuring-github-copilot/configuring-github-copilot-in-your-environment)
