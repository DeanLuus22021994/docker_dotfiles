agent: agent
model: 'Claude Sonnet 4'
---

<!-- markdownlint-disable-file -->

# Implementation Prompt: Docker Stack Hardening

## Implementation Instructions

### Step 1: Create Changes Tracking File

You WILL create `20251027-docker-stack-hardening-changes.md` in `.copilot-tracking/changes/` if it does not exist.

### Step 2: Execute Implementation

You WILL follow project standards from `.github/copilot-instructions.md`
You WILL implement tasks from `.copilot-tracking/plans/20251027-docker-stack-hardening-plan.instructions.md` sequentially, consulting `.copilot-tracking/details/20251027-docker-stack-hardening-details.md`
You WILL reference `.copilot-tracking/research/20251027-docker-stack-hardening-research.md` for verified context

**CRITICAL**: If ${input:phaseStop:true} is true, you WILL stop after each Phase for user review.
**CRITICAL**: If ${input:taskStop:false} is true, you WILL stop after each Task for user review.

### Step 3: Cleanup

When ALL Phases are checked off (`[x]`) and completed you WILL do the following:

1. You WILL provide a markdown style link and a summary of all changes from `.copilot-tracking/changes/20251027-docker-stack-hardening-changes.md` to the user:
   - You WILL keep the overall summary brief
   - You WILL add spacing around any lists
   - You MUST wrap any reference to a file in a markdown style link

2. You WILL provide markdown style links to `.copilot-tracking/plans/20251027-docker-stack-hardening-plan.instructions.md`, `.copilot-tracking/details/20251027-docker-stack-hardening-details.md`, and `.copilot-tracking/research/20251027-docker-stack-hardening-research.md` documents. You WILL recommend cleaning these files up as well.
3. **MANDATORY**: You WILL attempt to delete `.copilot-tracking/prompts/implement-docker-stack-hardening.prompt.md`

## Success Criteria

- [ ] Changes tracking file created and updated throughout execution
- [ ] All tasks in the plan completed with validated network, security, reliability, and observability improvements
- [ ] Documentation and CI updates reflect new controls and pass repository validation commands
- [ ] Final summary and cleanup instructions provided per Step 3
