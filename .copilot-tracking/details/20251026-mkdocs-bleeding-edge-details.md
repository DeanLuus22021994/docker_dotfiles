<!-- markdownlint-disable-file -->

# Task Details: MkDocs Bleeding-Edge Implementation

## Research Reference

**Source Research**: #file:../research/20251026-mkdocs-bleeding-edge-research.md

## Phase 1: Document Template Generator

### Task 1.1: Create Pydantic schema models for frontmatter validation

Implement comprehensive Pydantic v2 models for all documentation frontmatter fields with Python 3.14 features.

- **Files**:
  - .config/mkdocs/schemas/frontmatter.py - Pydantic models (NEW)
  - .config/mkdocs/schemas/**init**.py - Package init (NEW)
- **Success**:
  - All frontmatter fields have Pydantic models with validators
  - Date fields use ISO 8601 format with timezone awareness
  - Tags validated against allowed list
  - Description length constrained (20-160 chars for SEO)
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 30-52) - Frontmatter requirements
  - #githubRepo:\"pydantic/pydantic Python 3.14 dataclass integration\" - Modern patterns
- **Dependencies**: None

**Implementation Pattern**:

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from pydantic import BaseModel, Field, field_validator, model_validator

@dataclass(frozen=True, slots=True)
class FrontmatterConfig:
    required_fields: list[str]
    allowed_tags: list[str]
    description_min: int = 20
    description_max: int = 160

class DocFrontmatter(BaseModel):
    date_created: datetime = Field(..., description=\"ISO 8601 creation date\")
    last_updated: datetime = Field(..., description=\"ISO 8601 update date\")
    tags: list[str] = Field(..., min_length=1, max_length=10)
    description: str = Field(..., min_length=20, max_length=160)

    @field_validator('date_created', 'last_updated')
    @classmethod
    def validate_dates(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        allowed = {\"docker\", \"platform\", \"index\", \"documentation\", ...}
        invalid = set(v) - allowed
        if invalid:
            raise ValueError(f\"Invalid tags: {invalid}\")
        return v
```

### Task 1.2: Implement interactive CLI with rich/inquirer for template selection

Create user-friendly CLI tool for generating documentation files with interactive prompts.

- **Files**:
  - .config/mkdocs/scripts/new_doc.py - Template generator CLI (NEW)
  - .config/mkdocs/templates/ - Jinja2 templates directory (NEW)
- **Success**:
  - Interactive category selection (readme/, agent/, api/, etc.)
  - Prompted for title, description, tags
  - Auto-generates valid frontmatter with current timestamps
  - Creates file in correct directory with proper naming
  - Rich formatting with progress indicators
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 54-78) - CLI requirements
  - #githubRepo:\"Textualize/rich Python rich console output\" - Rich library patterns
- **Dependencies**: Task 1.1 (Pydantic models)

**Implementation Pattern**:

```python
#!/usr/bin/env python3
\"\"\"Document template generator with interactive CLI.

Usage:
    python .config/mkdocs/scripts/new_doc.py
    python .config/mkdocs/scripts/new_doc.py --category readme --title \"Setup Guide\"
\"\"\"

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import inquirer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..schemas.frontmatter import DocFrontmatter

@dataclass(frozen=True, slots=True)
class DocCategory:
    name: str
    path: Path
    template: str
    description: str

CATEGORIES: list[DocCategory] = [
    DocCategory(\"readme\", Path(\"docs/readme\"), \"readme.j2\", \"Getting started documentation\"),
    DocCategory(\"agent\", Path(\"docs/agent\"), \"agent.j2\", \"AI agent development guides\"),
    DocCategory(\"api\", Path(\"docs/api\"), \"api.j2\", \"API reference documentation\"),
    DocCategory(\"index\", Path(\"docs/index\"), \"index.j2\", \"Index and overview pages\"),
]

def interactive_prompt() -> DocFrontmatter:
    \"\"\"Run interactive CLI prompts for doc creation.\"\"\"
    console = Console()

    questions = [
        inquirer.List('category', message=\"Select documentation category\",
                     choices=[(c.description, c.name) for c in CATEGORIES]),
        inquirer.Text('title', message=\"Document title\"),
        inquirer.Text('description', message=\"Brief description (20-160 chars)\"),
        inquirer.Checkbox('tags', message=\"Select tags\",
                         choices=[\"docker\", \"platform\", \"setup\", \"guide\"]),
    ]

    answers = inquirer.prompt(questions)

    # Create frontmatter with validation
    now = datetime.now(timezone.utc)
    frontmatter = DocFrontmatter(
        date_created=now,
        last_updated=now,
        tags=answers['tags'],
        description=answers['description']
    )

    return answers['category'], answers['title'], frontmatter
```

### Task 1.3: Add template rendering with Jinja2 for doc categories

Create Jinja2 templates for each documentation category with proper structure.

- **Files**:
  - .config/mkdocs/templates/readme.j2 - README template (NEW)
  - .config/mkdocs/templates/agent.j2 - Agent docs template (NEW)
  - .config/mkdocs/templates/api.j2 - API docs template (NEW)
  - .config/mkdocs/templates/base.j2 - Base template with frontmatter (NEW)
- **Success**:
  - All templates extend base.j2 for frontmatter consistency
  - Category-specific content structure
  - Proper markdown formatting with headings, code blocks
  - Template variables for title, description, tags
  - Auto-generated boilerplate (quick start, examples, etc.)
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 80-105) - Template requirements
- **Dependencies**: Task 1.2 (CLI implementation)

**Template Pattern (base.j2)**:

```jinja2
---
date_created: \"{{ date_created.isoformat() }}\"
last_updated: \"{{ last_updated.isoformat() }}\"
tags: {{ tags | tojson }}
description: \"{{ description }}\"
---

# {{ title }}

{{ description }}

{% block content %}
## Overview

[Add overview content here]

## Quick Start

[Add quick start instructions]

## Features

- Feature 1
- Feature 2

## Usage

[Add usage examples]

## Related Documentation

- [Related Doc 1](../path/to/doc.md)

{% endblock %}
```

### Task 1.4: Integrate .pages file generation for awesome-pages plugin

Auto-update .pages files when creating new docs for seamless navigation.

- **Files**:
  - .config/mkdocs/scripts/new_doc.py - Update with .pages logic
  - docs/\*\*/.pages - Auto-generated nav files
- **Success**:
  - New doc automatically added to .pages in correct order
  - Title from frontmatter used for nav display
  - Natural sorting maintained (readme/ first, then alphabetical)
  - Existing .pages preserved with new entry appended
  - Validation that .pages remains valid YAML
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 107-125) - Awesome-pages integration
  - #githubRepo:\"lukasgeiter/mkdocs-awesome-pages-plugin .pages format\" - Plugin documentation
- **Dependencies**: Task 1.3 (Template rendering)

**Implementation Pattern**:

```python
def update_pages_file(category_path: Path, filename: str, title: str) -> None:
    \"\"\"Update .pages file with new document entry.\"\"\"
    pages_file = category_path / \".pages\"

    if pages_file.exists():
        with open(pages_file, 'r') as f:
            pages = yaml.safe_load(f) or {}
    else:
        pages = {\"nav\": []}

    # Add new entry with title from frontmatter
    pages[\"nav\"].append({title: filename})

    # Write back with natural sorting
    with open(pages_file, 'w') as f:
        yaml.dump(pages, f, default_flow_style=False, sort_keys=False)
```

### Task 1.5: Add VS Code snippet integration and testing

Create VS Code snippet for quick doc generation and comprehensive test suite.

- **Files**:
  - .vscode/snippets/markdown.code-snippets - Markdown doc snippets (UPDATE)
  -     ests/config/mkdocs/test_new_doc.py - Unit tests (NEW)
- **Success**:
  - VS Code snippet triggers with mkdocs-new prefix
  - Snippet runs new_doc.py script
  - Tests cover all doc categories
  - Tests validate frontmatter generation
  - Tests verify .pages file updates
  - 95%+ test coverage for new_doc.py
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 127-150) - Testing requirements
- **Dependencies**: Task 1.4 (.pages integration)

## Phase 2: Strict Mode Validation

### Task 2.1: Audit all existing docs for frontmatter compliance

Scan all markdown files in docs/ for missing or invalid frontmatter.

- **Files**:
  - .config/mkdocs/scripts/audit_docs.py - Audit script (NEW)
  - docs/\*_/_.md - All documentation files
- **Success**:
  - Report generated listing all non-compliant docs
  - Categories: missing frontmatter, invalid dates, invalid tags, short descriptions
  - JSON output for programmatic processing
  - Console output with rich formatting
  - Summary statistics (X/Y docs compliant)
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 152-175) - Audit requirements
- **Dependencies**: None

**Implementation Pattern**:

```python
from pathlib import Path
from typing import TypeAlias

import frontmatter
from rich.table import Table

AuditResult: TypeAlias = dict[str, list[str]]

def audit_frontmatter(docs_dir: Path) -> AuditResult:
    \"\"\"Audit all docs for frontmatter compliance.\"\"\"
    results: AuditResult = {
        \"missing\": [],
        \"invalid_dates\": [],
        \"invalid_tags\": [],
        \"short_description\": []
    }

    for md_file in docs_dir.rglob(\"*.md\"):
        post = frontmatter.load(md_file)

        if not post.metadata:
            results[\"missing\"].append(str(md_file))
            continue

        # Validate each field with Pydantic
        try:
            DocFrontmatter(**post.metadata)
        except ValueError as e:
            # Categorize error
            pass

    return results
```

### Task 2.2: Fix validation errors and standardize frontmatter

Update all non-compliant docs with valid frontmatter using automated fixes.

- **Files**:
  - .config/mkdocs/scripts/fix_frontmatter.py - Auto-fix script (NEW)
  - docs/\*_/_.md - Updated documentation files
- **Success**:
  - All docs have valid frontmatter after fixes
  - Missing frontmatter added with sensible defaults
  - Invalid dates converted to ISO 8601 format
  - Tags standardized to allowed list
  - Descriptions extended if too short
  - Backup created before modifications
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 177-200) - Fix automation
- **Dependencies**: Task 2.1 (Audit results)

### Task 2.3: Enable `strict: true` in mkdocs.yml with error handling

Turn on strict mode validation with graceful error reporting.

- **Files**:
  - .config/mkdocs/mkdocs.yml - Update strict setting (line 43)
  - .config/mkdocs/base.yml - Configure validation rules
- **Success**:
  - `strict: true` enabled
  - Nav warnings → errors
  - Broken links → fail build
  - Missing meta → warnings (not errors)
  - Build errors include file path and line number
  - CI/CD fails on strict mode violations
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 202-225) - Strict mode config
  - #fetch:https://www.mkdocs.org/user-guide/configuration/#strict - Official docs
- **Dependencies**: Task 2.2 (All docs fixed)

### Task 2.4: Update linkcheck-skip.txt for legitimate external links

Configure link checker to skip rate-limited or flaky external URLs.

- **Files**:
  - .config/mkdocs/linkcheck-skip.txt - Skip list (UPDATE)
- **Success**:
  - GitHub API URLs skipped (rate-limited)
  - CDN URLs with CORS restrictions skipped
  - Docker Hub URLs skipped (flaky)
  - Internal links NOT skipped (always checked)
  - Comments explain why each URL skipped
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 227-250) - Linkcheck config
- **Dependencies**: Task 2.3 (Strict mode enabled)

### Task 2.5: Test build with strict mode and fix all warnings

Run full build with strict mode and resolve all validation issues.

- **Files**:
  - All documentation and config files
- **Success**:
  - `mkdocs build --strict` completes with exit code 0
  - Zero warnings in build output
  - All nav links resolve correctly
  - All cross-references valid
  - Search index generated successfully
  - Sitemap.xml valid
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 252-275) - Testing strategy
- **Dependencies**: Task 2.4 (Linkcheck configured)

## Phase 3: Enhanced Validation Hooks

### Task 3.1: Extend validate_frontmatter.py with Pydantic models

Replace basic validation with comprehensive Pydantic-based checks.

- **Files**:
  - .config/mkdocs/hooks/validate_frontmatter.py - Enhanced validation (UPDATE)
- **Success**:
  - Uses Pydantic models from schemas/frontmatter.py
  - Validates on every page during build
  - Detailed error messages with field names
  - MkDocs hook integration (on_page_markdown)
  - Fails build if validation error (strict mode)
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 277-300) - Hook implementation
  - #fetch:https://www.mkdocs.org/dev-guide/plugins/#events - MkDocs plugin events
- **Dependencies**: Phase 1 Task 1.1 (Pydantic models)

**Hook Pattern**:

```python
def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig,
                     files: Files) -> str | None:
    \"\"\"Validate frontmatter before markdown processing.\"\"\"
    try:
        DocFrontmatter(**page.meta)
    except ValidationError as e:
        if config['strict']:
            raise PluginError(f\"Invalid frontmatter in {page.file.src_path}: {e}\")
        else:
            log.warning(f\"Frontmatter warning in {page.file.src_path}: {e}\")

    return markdown
```

### Task 3.2: Add custom validators for dates, tags, description length

Implement domain-specific validation rules beyond Pydantic defaults.

- **Files**:
  - .config/mkdocs/schemas/validators.py - Custom validators (NEW)
- **Success**:
  - Date validator: ensures timezone-aware ISO 8601
  - Tag validator: checks against project taxonomy
  - Description validator: SEO length (20-160 chars)
  - URL validator: internal links use relative paths
  - Custom error messages for each validator
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 302-325) - Validator specs
- **Dependencies**: Task 3.1 (Pydantic integration)

### Task 3.3: Integrate validation hooks with MkDocs build process

Configure MkDocs to run validation automatically on every build.

- **Files**:
  - .config/mkdocs/hooks.yml - Hook configuration (UPDATE)
  - .config/mkdocs/mkdocs.yml - Import hooks config
- **Success**:
  - Hooks run before build starts
  - Early exit on critical validation errors
  - Performance impact <2 seconds for full build
  - Progress indicators during validation
  - Summary report at end of build
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 327-350) - Hook integration
- **Dependencies**: Task 3.2 (Custom validators)

### Task 3.4: Create pre-commit hook for frontmatter validation

Add Git pre-commit hook to validate frontmatter before commits.

- **Files**:
  - .pre-commit-config.yaml - Add frontmatter hook (UPDATE)
  - .config/mkdocs/scripts/validate_frontmatter_cli.py - CLI validator (UPDATE)
- **Success**:
  - Pre-commit runs on staged .md files only
  - Validates frontmatter with Pydantic models
  - Fails commit if validation errors
  - Fast execution (<1s for typical commit)
  - Can be skipped with --no-verify flag
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 352-375) - Pre-commit config
- **Dependencies**: Task 3.3 (Hook integration)

**Pre-commit Config**:

```yaml
- repo: local
  hooks:
    - id: validate-docs-frontmatter
      name: Validate Documentation Frontmatter
      entry: python .config/mkdocs/scripts/validate_frontmatter_cli.py
      language: python
      files: ^docs/.*\.md$
      pass_filenames: true
      additional_dependencies: [pydantic>=2.9.0, python-frontmatter>=1.1.0]
```

### Task 3.5: Add CI/CD workflow for documentation validation

Create GitHub Actions workflow to validate docs on every PR.

- **Files**:
  - .github/workflows/docs-validate.yml - Validation workflow (NEW)
- **Success**:
  - Runs on PR to main branch
  - Validates all docs with strict mode
  - Checks for broken links
  - Reports validation errors as PR comments
  - Blocks merge if validation fails
  - Caches dependencies for fast builds (<2min)
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 377-400) - CI/CD workflow
- **Dependencies**: Task 3.4 (Pre-commit hook)

## Phase 4: Build Metrics & Health Checks

### Task 4.1: Implement build_metrics.py with comprehensive tracking

Track detailed metrics during MkDocs build process.

- **Files**:
  - .config/mkdocs/hooks/build_metrics.py - Metrics tracking (UPDATE)
- **Success**:
  - Tracks page count, plugin execution time, asset sizes
  - Records build start/end timestamps
  - Measures incremental vs cold build time
  - Tracks search index size
  - Generates metrics.json with structured data
  - Console output with rich tables
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 402-425) - Metrics spec
- **Dependencies**: None

**Metrics Structure**:

```python
@dataclass(frozen=True, slots=True)
class BuildMetrics:
    timestamp: datetime
    duration_seconds: float
    page_count: int
    asset_size_mb: float
    search_index_kb: float
    plugin_times: dict[str, float]
    warnings_count: int
    errors_count: int
```

### Task 4.2: Add validate_health.py post-build verification

Verify site integrity after build completes.

- **Files**:
  - .config/mkdocs/scripts/validate_health.py - Health checks (UPDATE)
- **Success**:
  - Verifies critical files exist (index.html, sitemap.xml, search_index.json)
  - Checks all internal links resolve
  - Validates HTML syntax
  - Checks for missing images
  - Verifies JSON schema of search index
  - Returns exit code 1 if any check fails
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 427-450) - Health check spec
- **Dependencies**: Task 4.1 (Build metrics)

### Task 4.3: Generate metrics.json for dashboard integration

Output build metrics in machine-readable format for monitoring.

- **Files**:
  - site/metrics.json - Generated metrics file (OUTPUT)
  - .config/mkdocs/hooks/build_metrics.py - Metrics generator (UPDATE)
- **Success**:
  - JSON file generated in site/ directory
  - Includes all metrics from BuildMetrics dataclass
  - Timestamp in ISO 8601 format
  - Compatible with Grafana/Prometheus JSON importer
  - Historical metrics preserved in time-series format
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 452-475) - Dashboard integration
- **Dependencies**: Task 4.2 (Health validation)

### Task 4.4: Add performance budgets and threshold warnings

Set performance thresholds and warn when exceeded.

- **Files**:
  - .config/mkdocs/performance-budgets.yml - Budget configuration (NEW)
  - .config/mkdocs/hooks/build_metrics.py - Budget checking (UPDATE)
- **Success**:
  - Asset size budget: <10MB total
  - Search index budget: <500KB
  - Build time budget: <60s cold, <10s incremental
  - Page count budget: <1000 pages
  - Warnings logged if budgets exceeded
  - CI/CD fails if critical budgets exceeded
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 477-500) - Budget config
- **Dependencies**: Task 4.3 (Metrics generation)

### Task 4.5: Integrate health checks into Docker validation stage

Add health validation to Dockerfile validation stage.

- **Files**:
  - dockerfile/mkdocs.Dockerfile - Add health checks (UPDATE)
- **Success**:
  - Validation stage runs validate_health.py
  - Build fails if health checks fail
  - Validation layer only includes health script (minimal)
  - Health check output visible in build logs
  - Production stage only built if validation passes
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 502-525) - Docker integration
- **Dependencies**: Task 4.4 (Performance budgets)

## Phase 5: Bleeding-Edge Extensions

### Task 5.1: Configure interactive Mermaid v10+ diagrams

Enable latest Mermaid with interactive features.

- **Files**:
  - .config/mkdocs/markdown.yml - Add Mermaid config (UPDATE)
  - .config/mkdocs/assets/javascripts/mermaid-config.js - Mermaid init (NEW)
- **Success**:
  - Mermaid v10+ loaded from CDN
  - Interactive zoom/pan on diagrams
  - Dark mode support
  - Export to SVG/PNG
  - Sequence, class, ER, flowchart diagrams all work
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 527-550) - Mermaid config
  - #fetch:https://mermaid.js.org/config/setup/modules/mermaidAPI.html - Mermaid v10 API
- **Dependencies**: None

### Task 5.2: Add custom admonition types for Docker/Python/API

Create project-specific admonition styles.

- **Files**:
  - .config/mkdocs/assets/stylesheets/admonitions.css - Custom styles (UPDATE)
  - .config/mkdocs/markdown.yml - Register admonition types (UPDATE)
- **Success**:
  - Docker admonition with container icon
  - Python admonition with snake icon
  - API admonition with endpoint icon
  - Command admonition with terminal icon
  - Security admonition with lock icon
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 552-575) - Custom admonitions
- **Dependencies**: None

### Task 5.3: Enable social card templates with custom branding

Configure Open Graph image generation with project branding.

- **Files**:
  - .config/mkdocs/social-cards/default.html - Card template (NEW)
  - .config/mkdocs/assets/images/logo-og.png - OG logo (NEW)
  - .config/mkdocs/plugins.yml - Update social plugin config (UPDATE)
- **Success**:
  - Custom card layout with project logo
  - Dynamic text from page title/description
  - Gradient background matching theme
  - PNG images cached in .cache/plugin/social
  - Cards generated for all pages automatically
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 577-600) - Social cards
  - #fetch:https://squidfunk.github.io/mkdocs-material/plugins/social/ - Social plugin docs
- **Dependencies**: None

### Task 5.4: Configure progressive image loading and optimization

Add lazy loading and image optimization for better performance.

- **Files**:
  - .config/mkdocs/assets/javascripts/lazy-images.js - Lazy load script (NEW)
  - .config/mkdocs/hooks/optimize_images.py - Image optimizer (NEW)
- **Success**:
  - Images lazy load with IntersectionObserver
  - Placeholder blur while loading
  - Automatic WebP conversion
  - Image compression (80% quality)
  - Responsive srcset for different screen sizes
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 602-625) - Image optimization
- **Dependencies**: None

### Task 5.5: Add JSON-LD structured data for SEO

Embed structured data for better search engine understanding.

- **Files**:
  - .config/mkdocs/hooks/structured_data.py - JSON-LD generator (NEW)
  - .config/mkdocs/hooks.yml - Register hook (UPDATE)
- **Success**:
  - Article schema for all docs
  - BreadcrumbList schema for navigation
  - Organization schema for site
  - WebSite schema with search action
  - Valid structured data per Google validator
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 627-650) - Structured data
  - #fetch:https://schema.org/Article - Schema.org docs
- **Dependencies**: None

## Phase 6: Docker & DevOps Integration

### Task 6.1: Optimize Dockerfile for <20MB production images

Reduce production image size with advanced optimizations.

- **Files**:
  - dockerfile/mkdocs.Dockerfile - Optimize all stages (UPDATE)
- **Success**:
  - Production image <20MB (nginx:alpine base ~15MB)
  - Multi-stage build with BuildKit cache mounts
  - Static assets pre-compressed (gzip level 9)
  - Unnecessary files excluded (.git, tests, etc.)
  - Non-root nginx user for security
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 652-675) - Docker optimization
- **Dependencies**: None

### Task 6.2: Add GitHub Actions workflow for docs deployment

Automate documentation deployment on pushes to main.

- **Files**:
  - .github/workflows/docs-deploy.yml - Deployment workflow (NEW)
- **Success**:
  - Triggers on push to main (docs/ or .config/mkdocs/ changes)
  - Builds with validation stage
  - Deploys to GitHub Pages
  - Updates deployment status in PR
  - Caches Docker layers for fast builds
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 677-700) - CI/CD deployment
- **Dependencies**: Task 6.1 (Docker optimization)

### Task 6.3: Configure docker-compose with docs profile

Add MkDocs service to docker-compose for local development.

- **Files**:
  - docker-compose.yml - Add cluster-docs service (UPDATE)
- **Success**:
  - Service uses development target for live reload
  - Volumes mount docs/ and .config/mkdocs/
  - Port 8000 exposed for local access
  - Profile \"docs\" for optional startup
  - Health check verifies server running
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 702-725) - Compose integration
- **Dependencies**: Task 6.2 (CI/CD workflow)

### Task 6.4: Add Makefile targets for common doc operations

Create convenient make targets for documentation tasks.

- **Files**:
  - Makefile - Add docs targets (UPDATE)
- **Success**:
  - `make docs-new` - Create new doc with template
  - `make docs-serve` - Start development server
  - `make docs-build` - Build production site
  - `make docs-validate` - Run all validations
  - `make docs-deploy` - Deploy to GitHub Pages
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 727-750) - Make targets
- **Dependencies**: Task 6.3 (Docker Compose)

### Task 6.5: Test full CI/CD pipeline with validation gates

End-to-end testing of complete documentation workflow.

- **Files**:
  - All project files
- **Success**:
  - Create new doc with template → passes validation
  - Commit triggers pre-commit hook → validation succeeds
  - Push triggers CI → build succeeds with strict mode
  - Merge to main → auto-deploys to GitHub Pages
  - Production image <20MB
  - Build time <60s
  - Zero validation warnings/errors
- **Research References**:
  - #file:../research/20251026-mkdocs-bleeding-edge-research.md (Lines 752-775) - E2E testing
- **Dependencies**: Task 6.4 (Makefile targets)

---

**Total Implementation**: 30 tasks across 6 phases, estimated 120-150 hours of work
