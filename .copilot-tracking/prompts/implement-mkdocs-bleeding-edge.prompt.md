---
agent: ask
description: "Implementation prompt for MkDocs Bleeding-Edge feature enhancements"
model: Claude Sonnet 4
---

<!-- markdownlint-disable-file -->

# Implementation Prompt: MkDocs Bleeding-Edge Completion

## Implementation Instructions

### Step 1: Create Changes Tracking File

You WILL create `20251026-mkdocs-bleeding-edge-changes.md` in `.copilot-tracking/changes/` if it does not exist.

### Step 2: Execute Implementation

You WILL systematically implement the plan at `.copilot-tracking/plans/20251026-mkdocs-bleeding-edge-plan.instructions.md` task-by-task
You WILL follow ALL project standards and conventions from `.github/copilot-instructions.md`

**CRITICAL**: If ${input:phaseStop:true} is true, you WILL stop after each Phase for user review.
**CRITICAL**: If ${input:taskStop:false} is true, you WILL stop after each Task for user review.

### Step 3: Cleanup

When ALL Phases are checked off ([x]) and completed you WILL do the following:

1. You WILL provide a markdown style link and a summary of all changes from `.copilot-tracking/changes/20251026-mkdocs-bleeding-edge-changes.md` to the user:
   - You WILL keep the overall summary brief
   - You WILL add spacing around any lists
   - You MUST wrap any reference to a file in a markdown style link

2. You WILL provide markdown style links to the planning documents (plans/, details/, research/ in .copilot-tracking). You WILL recommend cleaning these files up as well.

3. **MANDATORY**: You WILL attempt to delete `.copilot-tracking/prompts/implement-mkdocs-bleeding-edge.prompt.md`

## Success Criteria

- [ ] Changes tracking file created
- [ ] All plan items implemented with working code
- [ ] All detailed specifications satisfied
- [ ] Project conventions followed
- [ ] Changes file updated continuously
