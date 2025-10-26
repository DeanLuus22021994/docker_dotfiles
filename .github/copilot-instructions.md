The following instructions are only to be applied when performing a code review.

## README updates

- [ ] The new file should be added to the `README.md`.

## Copilot Tracking Workflow

**Applies to all files in `.copilot-tracking/` directory**

### Research Files (`research/YYYYMMDD-task-description-research.md`)

- [ ] File name uses format: `YYYYMMDD-task-description-research.md`
- [ ] Contains comprehensive findings from tool usage (not hypothetical)
- [ ] Includes verified code examples and specifications
- [ ] References specific project files with line numbers where relevant
- [ ] Documents external sources with concrete implementation examples
- [ ] Provides implementation guidance based on evidence
- [ ] No template markers (`{{placeholder}}`) remain in final version

### Plan Files (`plans/YYYYMMDD-task-description-plan.instructions.md`)

- [ ] File name uses format: `YYYYMMDD-task-description-plan.instructions.md`
- [ ] Has frontmatter with `applyTo: '.copilot-tracking/changes/YYYYMMDD-task-description-changes.md'`
- [ ] Includes `<!-- markdownlint-disable-file -->` at top
- [ ] Contains Overview, Objectives, Research Summary sections
- [ ] Has Implementation Checklist with phases and tasks
- [ ] Each task links to details file with line numbers: `(Lines XX-YY)`
- [ ] Includes Dependencies and Success Criteria sections
- [ ] References validated research file
- [ ] No template markers remain in final version

### Details Files (`details/YYYYMMDD-task-description-details.md`)

- [ ] File name uses format: `YYYYMMDD-task-description-details.md`
- [ ] Includes `<!-- markdownlint-disable-file -->` at top
- [ ] Has Research Reference linking to source research file
- [ ] Contains detailed specs for each plan phase/task
- [ ] Lists specific files to create/modify
- [ ] Defines success criteria for each task
- [ ] References research file sections with line numbers
- [ ] Documents task dependencies
- [ ] No template markers remain in final version

### Prompt Files (`prompts/implement-task-description.prompt.md`)

- [ ] File name uses format: `implement-task-description.prompt.md`
- [ ] Has frontmatter with `mode: agent` and `model: 'Claude Sonnet 4'`
- [ ] Includes `<!-- markdownlint-disable-file -->` at top
- [ ] Contains clear implementation instructions
- [ ] References plan file for execution steps
- [ ] Defines success criteria for completion
- [ ] Instructs to create changes tracking file
- [ ] Specifies cleanup steps (summary, links, delete prompt)
- [ ] No template markers remain in final version

### Changes Files (`changes/YYYYMMDD-task-description-changes.md`)

- [ ] File name uses format: `YYYYMMDD-task-description-changes.md`
- [ ] Created by coder agent during implementation
- [ ] Logs all file operations (create, modify, delete)
- [ ] Records success criteria validation
- [ ] Documents deviations from plan
- [ ] Updated continuously throughout implementation

## Prompt file guide

**Only apply to files that end in `.prompt.md`**

- [ ] The prompt has markdown front matter.
- [ ] The prompt has a `mode` field specified of either `agent` or `ask`.
- [ ] The prompt has a `description` field.
- [ ] The `description` field is not empty.
- [ ] The `description` field value is wrapped in single quotes.
- [ ] The file name is lower case, with words separated by hyphens.
- [ ] Encourage the use of `tools`, but it's not required.
- [ ] Strongly encourage the use of `model` to specify the model that the prompt is optimised for.

## Instruction file guide

**Only apply to files that end in `.instructions.md`**

- [ ] The instruction has markdown front matter.
- [ ] The instruction has a `description` field.
- [ ] The `description` field is not empty.
- [ ] The `description` field value is wrapped in single quotes.
- [ ] The file name is lower case, with words separated by hyphens.
- [ ] The instruction has an `applyTo` field that specifies the file or files to which the instructions apply. If they wish to specify multiple file paths they should formated like `'**.js, **.ts'`.

## Agent file guide

**Only apply to files that end in `.agent.md`**

- [ ] The agent file has YAML front matter (not markdown front matter).
- [ ] The agent has a `description` field wrapped in single quotes.
- [ ] The agent has a `tools` field listing available tool names.
- [ ] The agent has a `model` field specifying the optimized model (e.g., 'Claude Sonnet 4').
- [ ] The file name is lower case, with words separated by hyphens.
- [ ] The agent clearly defines: Purpose, When to Use, What It Does, What It Won't Do.
- [ ] The agent specifies expected inputs and delivered outputs.
- [ ] The agent documents progress reporting and when to ask for help.

## Chat Mode file guide

**Only apply to files that end in `.chatmode.md`**

- [ ] The chat mode has markdown front matter.
- [ ] The chat mode has a `description` field.
- [ ] The `description` field is not empty.
- [ ] The `description` field value is wrapped in single quotes.
- [ ] The file name is lower case, with words separated by hyphens.
- [ ] Encourage the use of `tools`, but it's not required.
- [ ] Strongly encourage the use of `model` to specify the model that the chat mode is optimised for.
