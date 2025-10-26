# Copilot Tracking Workflow

Structured workflow for AI-assisted development using GitHub Copilot with research, planning, and implementation phases.

## Directory Structure

```
.copilot-tracking/
├── research/              # Comprehensive research findings
│   └── YYYYMMDD-task-description-research.md
├── plans/                 # Task checklists and implementation plans
│   └── YYYYMMDD-task-description-plan.instructions.md
├── details/               # Detailed specifications for each task
│   └── YYYYMMDD-task-description-details.md
├── prompts/               # Implementation prompts for coder agent
│   └── implement-task-description.prompt.md
└── changes/               # Change tracking logs (created during implementation)
    └── YYYYMMDD-task-description-changes.md
```

## Workflow Phases

### Phase 1: Research (task-planner agent)

**Goal:** Gather comprehensive, validated information before planning

**Activities:**

- Use tools to explore codebase and external sources
- Document verified findings (not hypothetical)
- Include code examples and specifications
- Reference specific files with line numbers
- Validate against project standards

**Output:** `research/YYYYMMDD-task-description-research.md`

**Validation:** Research must be comprehensive before proceeding to planning

### Phase 2: Planning (task-planner agent)

**Goal:** Create actionable implementation plans based on validated research

**Activities:**

- Create plan checklist with phases and tasks
- Write detailed specifications for each task
- Define success criteria and dependencies
- Reference research with specific line numbers
- Create implementation prompt

**Outputs:**

- `plans/YYYYMMDD-task-description-plan.instructions.md` - Task checklist
- `details/YYYYMMDD-task-description-details.md` - Task specifications
- `prompts/implement-task-description.prompt.md` - Execution prompt

**Validation:** All line number references must be accurate and current

### Phase 3: Implementation (coder agent)

**Goal:** Execute planned tasks systematically following project standards

**Activities:**

- Create changes tracking file
- Implement tasks phase-by-phase
- Update changes file continuously
- Validate against success criteria
- Stop for review after each phase (if requested)
- Provide summary and cleanup when complete

**Output:** `changes/YYYYMMDD-task-description-changes.md`

**Validation:** All acceptance criteria from details file must be met

## File Naming Conventions

**Research:** `YYYYMMDD-task-description-research.md`

- Example: `20251026-mkdocs-bleeding-edge-research.md`

**Plan:** `YYYYMMDD-task-description-plan.instructions.md`

- Example: `20251026-mkdocs-bleeding-edge-plan.instructions.md`

**Details:** `YYYYMMDD-task-description-details.md`

- Example: `20251026-mkdocs-bleeding-edge-details.md`

**Prompt:** `implement-task-description.prompt.md`

- Example: `implement-mkdocs-bleeding-edge.prompt.md`

**Changes:** `YYYYMMDD-task-description-changes.md`

- Example: `20251026-mkdocs-bleeding-edge-changes.md`

## Agent Roles

### task-planner agent

**Responsibilities:**

- Conduct comprehensive research
- Validate research completeness
- Create actionable plans
- Write detailed specifications
- Generate implementation prompts

**Tools:** All read/search tools, web search, GitHub repo search

**Boundaries:** Creates plans only, never implements code

### coder agent

**Responsibilities:**

- Execute planned tasks
- Track all changes
- Follow project standards
- Validate success criteria
- Provide completion summary

**Tools:** All tools including file creation/editing, commands, tests

**Boundaries:** Implements only from validated plans, never plans

## Input Variables

Prompts can include input variables for user control:

**`${input:phaseStop:true}`** - Stop after each Phase for review (default: true)
**`${input:taskStop:false}`** - Stop after each Task for review (default: false)

Example prompt:

```markdown
---
mode: agent
model: Claude Sonnet 4
---

**CRITICAL**: If ${input:phaseStop:true} is true, you WILL stop after each Phase for user review.
**CRITICAL**: If ${input:taskStop:false} is true, you WILL stop after each Task for user review.
```

## Line Number References

All cross-references between files must include line numbers for precision:

**Plan → Details:**

```markdown
- [ ] Task 1.1: Create Pydantic schema models
  - Details: .copilot-tracking/details/20251026-mkdocs-bleeding-edge-details.md (Lines 30-80)
```

**Details → Research:**

```markdown
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 30-52) - Frontmatter requirements
```

**When references become invalid:**

1. Identify current file structure
2. Update line number references
3. Verify content alignment
4. Update research if content no longer exists

## Template Placeholders

All templates use `{{placeholder}}` format with double curly braces:

**Format:** `{{descriptive_name}}` with snake_case names

**Common Placeholders:**

- `{{task_name}}` - Human-readable task name
- `{{date}}` - YYYYMMDD format date
- `{{file_path}}` - Absolute or relative file path
- `{{specific_action}}` - Concrete action description

**Critical:** NO template markers should remain in final files

## Integration with Project Standards

All implementation must follow:

**Code Review:** `.github/copilot-instructions.md`
**Language Standards:** `.github/instructions/*.instructions.md`
**Python:** `pyproject.toml` (PEP 585, dataclasses, strict typing)
**Linting:** `.pre-commit-config.yaml`
**Docker:** `docker-compose.yml` (cluster-\* naming)
**AI Workflow:** `AGENT.md`

## Example Workflow

**User Request:**
"Implement MkDocs bleeding-edge features"

**task-planner agent:**

1. Searches codebase for MkDocs implementation
2. Researches MkDocs Material best practices
3. Creates comprehensive research document
4. Validates research completeness
5. Creates plan with 6 phases, 30 tasks
6. Writes detailed specifications
7. Generates implementation prompt

**coder agent:**

1. Reads implementation prompt
2. Verifies all prerequisite files exist
3. Creates changes tracking file
4. Implements Phase 1 (5 tasks)
5. Updates changes file with all modifications
6. Stops for user review (phaseStop=true)
7. User approves, continues with Phase 2
8. Repeats until all 6 phases complete
9. Provides summary with markdown links
10. Deletes prompt file

## Cleanup

**After Successful Implementation:**

1. Review changes file for completeness
2. Optionally archive research/plan/details files
3. Delete prompt file (automatic)
4. Update project TODO/CHANGELOG

**Archival Strategy:**

- Keep research/plan/details for reference
- Or move to `docs/reports/` with date prefix
- Changes file provides implementation record

## Best Practices

**Research Phase:**

- Use tools extensively, avoid guessing
- Include concrete examples, not hypothetical
- Validate against existing project patterns
- Document external sources with URLs

**Planning Phase:**

- Break work into logical phases
- Make tasks small and actionable
- Include specific success criteria
- Maintain accurate line number references
- Use evidence from research, not assumptions

**Implementation Phase:**

- Follow plan strictly, don't improvise
- Update changes file continuously
- Stop for review when uncertain
- Validate against success criteria
- Request help when prerequisites missing

## References

**Agent Definitions:**

- `.github/agents/task-planner.agent.md` - Planning agent
- `.github/agents/coder.agent.md` - Implementation agent

**Project Standards:**

- `.github/copilot-instructions.md` - Review guidelines
- `.github/instructions/` - Language-specific standards
- `AGENT.md` - AI-optimized workflow patterns

**Example Implementation:**

- `.copilot-tracking/research/20251026-mkdocs-bleeding-edge-research.md`
- `.copilot-tracking/plans/20251026-mkdocs-bleeding-edge-plan.instructions.md`
- `.copilot-tracking/details/20251026-mkdocs-bleeding-edge-details.md`
- `.copilot-tracking/prompts/implement-mkdocs-bleeding-edge.prompt.md`

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-26  
**Status:** Production Ready
