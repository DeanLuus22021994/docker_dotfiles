# Project TODO - v4.0

**Last Updated:** 2025-10-25  
**Current Phase:** v4.0 - Testing Infrastructure & Production Readiness  
**Status:** 🚀 IN PROGRESS

---

## 📊 Quick Status

| Category | Status | Progress | Priority |
|----------|--------|----------|----------|
| Testing Infrastructure | 🟡 Not Started | 0/6 | 🔴 Critical |
| Security Hardening | 🟡 Not Started | 0/6 | 🔴 Critical |
| Planned Scripts | 🟡 Not Started | 0/6 | 🟠 High |
| Documentation Consolidation | 🟡 Not Started | 0/4 | 🟠 High |
| Code Quality Automation | 🟡 Not Started | 0/3 | 🟢 Medium |
| Web Dashboard Enhancements | 🟡 Not Started | 0/5 | 🟢 Medium |

**Legend:**  
🟢 Complete | 🔵 In Progress | 🟡 Not Started | 🔴 Blocked | ⚪ Optional

---

## 🎯 Phase 4.1: Testing Infrastructure (Critical)

**Goal:** Establish comprehensive testing framework for Python scripts  
**Priority:** 🔴 CRITICAL  
**Target:** Week 1

### Tasks

#### 4.1.1 Setup pytest Framework ⚪ NOT STARTED
**Description:** Install and configure pytest for Python 3.14  
**Acceptance Criteria:**
- [ ] pytest installed with all plugins (pytest-cov, pytest-mock, pytest-asyncio)
- [ ] `pyproject.toml` updated with pytest configuration
- [ ] Test discovery working for `tests/` directory
- [ ] Coverage reporting configured (>80% target)

**Dependencies:** None  
**Estimated Time:** 1 hour

---

#### 4.1.2 Create Test Structure ⚪ NOT STARTED
**Description:** Create comprehensive test directory structure  
**Acceptance Criteria:**
- [ ] `tests/python/` directory created with `__init__.py`
- [ ] `tests/python/audit/` for code_quality.py and dependencies.py tests
- [ ] `tests/python/utils/` for colors.py, file_utils.py, logging_utils.py tests
- [ ] `tests/python/validation/` for validate_env.py and validate_configs.py tests
- [ ] `tests/fixtures/` for test data (sample configs, .env files)

**Structure:**
```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures
├── fixtures/
│   ├── sample.env              # Test environment file
│   ├── test-nginx.conf         # Test nginx config
│   ├── test-postgres.conf      # Test postgres config
│   └── test-pyproject.toml     # Test pyproject.toml
└── python/
    ├── __init__.py
    ├── audit/
    │   ├── __init__.py
    │   ├── test_code_quality.py
    │   └── test_dependencies.py
    ├── utils/
    │   ├── __init__.py
    │   ├── test_colors.py
    │   ├── test_file_utils.py
    │   └── test_logging_utils.py
    └── validation/
        ├── __init__.py
        ├── test_validate_env.py
        └── test_validate_configs.py
```

**Dependencies:** 4.1.1  
**Estimated Time:** 1 hour

---

#### 4.1.3 Write Unit Tests for Utils ⚪ NOT STARTED
**Description:** Write comprehensive unit tests for utils module  
**Acceptance Criteria:**
- [ ] `test_colors.py` - Test all color output functions, terminals with/without ANSI support
- [ ] `test_file_utils.py` - Test find_files(), safe_read_file(), ensure_directory()
- [ ] `test_logging_utils.py` - Test all logging functions, log levels, formatters
- [ ] All tests passing with >90% coverage for utils module

**Key Test Cases:**
- Colors: ANSI escape codes, non-ANSI terminals, success/error/warning/info
- File Utils: File existence, directory creation, recursive search, error handling
- Logging: Setup logger, log levels, file handlers, console handlers

**Dependencies:** 4.1.2  
**Estimated Time:** 3 hours

---

#### 4.1.4 Write Unit Tests for Validation ⚪ NOT STARTED
**Description:** Write comprehensive unit tests for validation module  
**Acceptance Criteria:**
- [ ] `test_validate_env.py` - Test .env parsing, variable validation, missing variables detection
- [ ] `test_validate_configs.py` - Test config file validation, nginx/postgres/mariadb configs
- [ ] All tests passing with >90% coverage for validation module
- [ ] Mock Docker commands (don't require Docker installed)

**Key Test Cases:**
- Validate Env: Valid .env, missing required vars, malformed .env, empty values
- Validate Configs: Valid configs, invalid syntax, missing files, Docker validation

**Dependencies:** 4.1.2  
**Estimated Time:** 3 hours

---

#### 4.1.5 Write Unit Tests for Audit ⚪ NOT STARTED
**Description:** Write comprehensive unit tests for audit module  
**Acceptance Criteria:**
- [ ] `test_code_quality.py` - Test Black/Ruff/mypy execution, output parsing
- [ ] `test_dependencies.py` - Test dependency scanning, vulnerability checks
- [ ] All tests passing with >90% coverage for audit module
- [ ] Mock external tool execution (Black, Ruff, mypy)

**Key Test Cases:**
- Code Quality: Tool availability, successful runs, error handling, output parsing
- Dependencies: Package detection, version checking, vulnerability scanning

**Dependencies:** 4.1.2  
**Estimated Time:** 3 hours

---

#### 4.1.6 Setup CI/CD Testing Pipeline ⚪ NOT STARTED
**Description:** Add automated testing to GitHub Actions  
**Acceptance Criteria:**
- [ ] `.github/workflows/python-tests.yml` created
- [ ] Runs pytest on every push/PR
- [ ] Coverage reports generated and uploaded
- [ ] Failing tests block PR merges
- [ ] Badge added to README.md showing test status

**Workflow Steps:**
1. Checkout code
2. Setup Python 3.14
3. Install dependencies (uv sync)
4. Run pytest with coverage
5. Upload coverage to Codecov/Coveralls
6. Fail if coverage <80%

**Dependencies:** 4.1.3, 4.1.4, 4.1.5  
**Estimated Time:** 2 hours

---

## 🔒 Phase 4.2: Security Hardening (Critical)

**Goal:** Production-ready security for web dashboard and services  
**Priority:** 🔴 CRITICAL  
**Target:** Week 2

### Current Security Gaps (from analysis)

**Web Dashboard:**
- ❌ No authentication layer (OAuth, JWT, Basic Auth)
- ❌ No rate limiting beyond nginx defaults
- ❌ No HTTPS enforcement
- ❌ Direct service URLs exposed in frontend
- ❌ Port information visible to users

**API Endpoints:**
- ⚠️ Docker socket mounted (read-only, but needs audit)
- ⚠️ No request validation
- ⚠️ No API authentication
- ⚠️ CORS enabled for all origins

**References:**
- `web-content/INSTALL.md:205` - Security considerations section
- `web-content/ARCHITECTURE.md:268` - Production recommendations
- `api/README.md:58` - Security considerations
- `SECURITY.md:116` - Security features

### Tasks

#### 4.2.1 Implement Authentication Layer ⚪ NOT STARTED
**Description:** Add authentication to web dashboard  
**Acceptance Criteria:**
- [ ] Choose auth method (OAuth 2.0, JWT, or Basic Auth for internal)
- [ ] Implement auth middleware in `api/server.js`
- [ ] Add login page to `web-content/`
- [ ] Store tokens securely (httpOnly cookies or localStorage)
- [ ] Redirect unauthenticated users to login
- [ ] Document authentication setup in `web-content/SECURITY.md`

**Recommended:** JWT with refresh tokens for internal use, OAuth for production

**Files to Modify:**
- `api/server.js` - Add auth middleware
- `web-content/src/` - Add login component
- `web-content/src/services/dockerAPI.ts` - Add auth headers
- `.env.example` - Add JWT_SECRET, AUTH_ENABLED

**Dependencies:** None  
**Estimated Time:** 6 hours

---

#### 4.2.2 Add Rate Limiting ⚪ NOT STARTED
**Description:** Implement rate limiting for API endpoints  
**Acceptance Criteria:**
- [ ] Install `express-rate-limit` package
- [ ] Configure rate limits: 100 requests per 15 min for /api/*
- [ ] Configure stricter limits: 10 requests per 15 min for /api/containers/:id/stats
- [ ] Add rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining)
- [ ] Return 429 Too Many Requests on limit exceeded
- [ ] Document rate limits in `api/README.md`

**Configuration:**
```javascript
// api/server.js
const rateLimit = require('express-rate-limit');

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later.'
});

app.use('/api/', apiLimiter);
```

**Dependencies:** None  
**Estimated Time:** 2 hours

---

#### 4.2.3 Enable HTTPS & Reverse Proxy ⚪ NOT STARTED
**Description:** Setup HTTPS for production deployment  
**Acceptance Criteria:**
- [ ] Create `dockerfile/traefik.Dockerfile` for reverse proxy
- [ ] Configure Traefik for automatic HTTPS (Let's Encrypt)
- [ ] Update `docker-compose.yml` with Traefik service
- [ ] Redirect HTTP to HTTPS
- [ ] Add HSTS headers
- [ ] Document HTTPS setup in `docs/production-deployment.md`

**Services to Proxy:**
- Web Dashboard (port 80 → 443)
- API Server (port 3001 → 443/api)
- Grafana (port 3000 → 443/grafana)
- Jupyter (port 8888 → 443/jupyter)

**Dependencies:** None  
**Estimated Time:** 4 hours

---

#### 4.2.4 API Request Validation ⚪ NOT STARTED
**Description:** Add input validation and sanitization  
**Acceptance Criteria:**
- [ ] Install `express-validator` package
- [ ] Validate container ID format (alphanumeric, 12-64 chars)
- [ ] Sanitize all user inputs
- [ ] Return 400 Bad Request on invalid input
- [ ] Add validation middleware to all endpoints
- [ ] Document validation rules in `api/README.md`

**Validation Rules:**
- Container ID: `/^[a-f0-9]{12,64}$/`
- Query parameters: Whitelist allowed values
- Headers: Validate Content-Type, Accept

**Dependencies:** None  
**Estimated Time:** 2 hours

---

#### 4.2.5 Restrict CORS Origins ⚪ NOT STARTED
**Description:** Configure CORS for specific origins only  
**Acceptance Criteria:**
- [ ] Update CORS config in `api/server.js`
- [ ] Whitelist allowed origins (localhost:3000, production domain)
- [ ] Deny all other origins
- [ ] Add CORS_ORIGIN environment variable
- [ ] Document CORS configuration in `api/README.md`

**Configuration:**
```javascript
// api/server.js
const cors = require('cors');

const corsOptions = {
  origin: process.env.CORS_ORIGIN?.split(',') || ['http://localhost:3000'],
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

**Dependencies:** None  
**Estimated Time:** 1 hour

---

#### 4.2.6 Docker Socket Security Audit ⚪ NOT STARTED
**Description:** Audit and document Docker socket security  
**Acceptance Criteria:**
- [ ] Verify socket mounted read-only in all services
- [ ] Document socket permissions in `SECURITY.md`
- [ ] Add alternative: Docker API over TCP with TLS
- [ ] Create `docs/docker-socket-security.md` guide
- [ ] Consider Docker socket proxy (tecnativa/docker-socket-proxy)

**Socket Proxy Benefits:**
- Whitelists allowed API endpoints
- No full socket access required
- Better audit trail
- Defense in depth

**Dependencies:** None  
**Estimated Time:** 3 hours

---

## 🛠️ Phase 4.3: Implement Planned Scripts (High Priority)

**Goal:** Complete all planned scripts documented in READMEs  
**Priority:** 🟠 HIGH  
**Target:** Week 3

### PowerShell Scripts (Windows)

#### 4.3.1 cleanup/remove-old-images.ps1 ⚪ NOT STARTED
**Description:** Remove old/unused Docker images to reclaim disk space  
**Acceptance Criteria:**
- [ ] List all images with created date and size
- [ ] Filter images older than X days (default: 30)
- [ ] Exclude images tagged 'latest' or in use by running containers
- [ ] Interactive prompt before deletion (unless -Force)
- [ ] Display total space reclaimed
- [ ] Add to `scripts/powershell/cleanup/` directory
- [ ] Document in `scripts/powershell/README.md`

**Features:**
- `-DaysOld` parameter (default: 30)
- `-Force` switch to skip confirmation
- `-WhatIf` to preview deletions
- Color-coded output (red: deletable, green: kept)

**Reference:** CLEANUP-REPORT.md recommendations  
**Dependencies:** None  
**Estimated Time:** 2 hours

---

#### 4.3.2 cleanup/clear-volumes.ps1 ⚪ NOT STARTED
**Description:** Clear unused Docker volumes safely  
**Acceptance Criteria:**
- [ ] List all volumes with size and mount status
- [ ] Identify volumes not attached to any containers
- [ ] Interactive prompt showing volumes to delete
- [ ] Exclude volumes with specific labels (production, backup)
- [ ] Display total space reclaimed
- [ ] Add to `scripts/powershell/cleanup/` directory
- [ ] Document in `scripts/powershell/README.md`

**Features:**
- `-UnusedOnly` switch (default: true)
- `-Force` switch to skip confirmation
- `-ExcludePattern` to exclude volumes by name pattern
- Dry-run mode with `-WhatIf`

**Dependencies:** None  
**Estimated Time:** 2 hours

---

#### 4.3.3 audit/security-scan.ps1 ⚪ NOT STARTED
**Description:** Security vulnerability scan for Docker images and dependencies  
**Acceptance Criteria:**
- [ ] Scan Docker images with Trivy or Grype
- [ ] Scan Python dependencies with `pip-audit`
- [ ] Scan npm dependencies with `npm audit`
- [ ] Generate security report (HTML + JSON)
- [ ] Fail if critical vulnerabilities found (CI/CD integration)
- [ ] Add to `scripts/powershell/audit/` directory
- [ ] Document in `scripts/powershell/README.md`

**Scan Tools:**
1. Docker Images: `docker scan` or Trivy
2. Python: `pip-audit` (already in dependencies.py)
3. Node.js: `npm audit --json`
4. Secrets: `gitleaks` or `trufflehog`

**Dependencies:** Install Trivy/Grype  
**Estimated Time:** 4 hours

---

### Bash Scripts (Linux/macOS)

#### 4.3.4 docker/build-images.sh ⚪ NOT STARTED
**Description:** Build all Docker images with BuildKit optimization  
**Acceptance Criteria:**
- [ ] Read image list from `dockerfile/` directory
- [ ] Build images in parallel (max 4 concurrent)
- [ ] Use BuildKit cache mounts
- [ ] Tag images with git commit SHA and 'latest'
- [ ] Display build progress and total time
- [ ] Add to `scripts/bash/docker/` directory
- [ ] Document in `scripts/bash/README.md`

**Features:**
- `--no-cache` flag to force rebuild
- `--push` flag to push to registry
- `--image <name>` to build single image
- Colored output (green: success, red: failure)

**Dependencies:** BuildKit enabled  
**Estimated Time:** 3 hours

---

#### 4.3.5 docker/cleanup-volumes.sh ⚪ NOT STARTED
**Description:** Bash equivalent of PowerShell clear-volumes.ps1  
**Acceptance Criteria:**
- [ ] List unused volumes with `docker volume ls`
- [ ] Filter volumes not attached to containers
- [ ] Interactive confirmation before deletion
- [ ] Display space reclaimed
- [ ] Add to `scripts/bash/docker/` directory
- [ ] Document in `scripts/bash/README.md`

**Features:**
- `--force` flag to skip confirmation
- `--dry-run` to preview deletions
- Exclude volumes by pattern

**Dependencies:** None  
**Estimated Time:** 1 hour

---

#### 4.3.6 docs/build-docs.sh ⚪ NOT STARTED
**Description:** Build static documentation site with Jekyll or MkDocs  
**Acceptance Criteria:**
- [ ] Choose documentation tool (MkDocs recommended)
- [ ] Create `mkdocs.yml` configuration
- [ ] Convert existing Markdown to MkDocs format
- [ ] Build static site to `docs/site/`
- [ ] Add search functionality
- [ ] Add to `scripts/bash/docs/` directory
- [ ] Document in `scripts/bash/README.md`

**Documentation Structure:**
```
docs/
├── index.md (README.md)
├── setup.md (SETUP.md)
├── security.md (SECURITY.md)
├── agent.md (AGENT.md)
├── web-content/
│   ├── quickstart.md
│   ├── install.md
│   └── architecture.md
└── scripts/
    ├── python.md
    ├── powershell.md
    └── bash.md
```

**Dependencies:** Install MkDocs  
**Estimated Time:** 4 hours

---

## 📚 Phase 4.4: Documentation Consolidation (High Priority)

**Goal:** Organize documentation into single source of truth  
**Priority:** 🟠 HIGH  
**Target:** Week 4

### Current Issues (from CLEANUP-REPORT.md)

**Scattered Documentation:**
- Root: README.md, SETUP.md, AGENT.md, SECURITY.md, CLEANUP-REPORT.md
- web-content: 5 docs (README, ARCHITECTURE, IMPLEMENTATION, REFACTOR-SUMMARY, INSTALL, QUICKSTART)
- .config: README, github/README
- No clear hierarchy or index

**Obsolete Documentation:**
- ⚠️ ENHANCEMENTS-COMPLETE.md (review for archival)
- ⚠️ ENVIRONMENT-INTEGRATION-COMPLETE.md (review for archival)
- ⚠️ CLUSTER.md (consolidate into README or archive)

### Tasks

#### 4.4.1 Create Documentation Index ⚪ NOT STARTED
**Description:** Create centralized documentation index  
**Acceptance Criteria:**
- [ ] Create `docs/INDEX.md` with all documentation links
- [ ] Organize by category (Setup, Development, Architecture, Scripts)
- [ ] Add descriptions for each document
- [ ] Create quick reference section
- [ ] Link from main README.md
- [ ] Update all docs to reference INDEX.md

**Structure:**
```markdown
# Documentation Index

## 🚀 Getting Started
- [README](../README.md) - Project overview
- [SETUP](../SETUP.md) - Installation guide
- [Quickstart](web-content/quickstart.md) - 5-minute setup

## 🏗️ Architecture
- [Web Dashboard Architecture](web-content/architecture.md)
- [Docker Cluster Design](CLUSTER.md)
- [Security Policy](../SECURITY.md)

## 🛠️ Development
- [Scripts Guide](scripts/README.md)
- [AI Agent Development](../AGENT.md)
- [Migration Guide](scripts/MIGRATION.md)

## 📊 Monitoring
- [Grafana Dashboards](.config/monitoring/README.md)
- [Prometheus Config](.config/monitoring/prometheus/README.md)
```

**Dependencies:** None  
**Estimated Time:** 2 hours

---

#### 4.4.2 Archive Obsolete Documentation ⚪ NOT STARTED
**Description:** Review and archive completed/obsolete docs  
**Acceptance Criteria:**
- [ ] Review ENHANCEMENTS-COMPLETE.md for unique content
- [ ] Review ENVIRONMENT-INTEGRATION-COMPLETE.md for unique content
- [ ] Review CLUSTER.md vs README.md (consolidate or archive)
- [ ] Move archived docs to `.github/archive/`
- [ ] Add archive date to filename
- [ ] Update references in other docs
- [ ] Document archival in CHANGELOG.md

**Archive Candidates:**
- `ENHANCEMENTS-COMPLETE.md` → `.github/archive/ENHANCEMENTS-v2.0-20251025.md`
- `ENVIRONMENT-INTEGRATION-COMPLETE.md` → `.github/archive/ENVIRONMENT-v2.0-20251025.md`
- `CLUSTER.md` → Consolidate into README or `.github/archive/CLUSTER-v3.0-20251025.md`

**Dependencies:** 4.4.1 (update index after archival)  
**Estimated Time:** 2 hours

---

#### 4.4.3 Consolidate Web-Content Docs ⚪ NOT STARTED
**Description:** Reduce 5 web-content docs to 3 essential docs  
**Acceptance Criteria:**
- [ ] Keep: ARCHITECTURE.md (technical deep dive)
- [ ] Keep: INSTALL.md (installation guide)
- [ ] Merge: QUICKSTART.md + README.md → README.md (overview + quick start)
- [ ] Archive: IMPLEMENTATION.md (completed work, archive to .github/archive/)
- [ ] Archive: REFACTOR-SUMMARY.md (completed work, archive to .github/archive/)
- [ ] Update all cross-references
- [ ] Test all links work

**Rationale:**
- QUICKSTART + README overlap significantly
- IMPLEMENTATION & REFACTOR-SUMMARY document completed work (archive)
- ARCHITECTURE covers technical details
- INSTALL covers setup procedures

**Dependencies:** 4.4.2  
**Estimated Time:** 3 hours

---

#### 4.4.4 Create MkDocs Site ⚪ NOT STARTED
**Description:** Build searchable static documentation site  
**Acceptance Criteria:**
- [ ] Install MkDocs with Material theme
- [ ] Create `mkdocs.yml` configuration
- [ ] Add all markdown files to site
- [ ] Configure navigation structure
- [ ] Add search functionality
- [ ] Build and test locally (`mkdocs serve`)
- [ ] Deploy to GitHub Pages or docs/ folder
- [ ] Add link to README.md

**MkDocs Config:**
```yaml
site_name: Modern Data Platform
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest
    - search.highlight

nav:
  - Home: index.md
  - Setup: setup.md
  - Web Dashboard:
    - Installation: web-content/install.md
    - Architecture: web-content/architecture.md
  - Scripts:
    - Overview: scripts/README.md
    - Python: scripts/python/README.md
    - PowerShell: scripts/powershell/README.md
    - Bash: scripts/bash/README.md
  - Security: security.md
  - AI Agent: agent.md
```

**Dependencies:** 4.4.1, 4.4.2, 4.4.3  
**Estimated Time:** 4 hours

---

## ⚙️ Phase 4.5: Code Quality Automation (Medium Priority)

**Goal:** Automate code quality checks in CI/CD  
**Priority:** 🟢 MEDIUM  
**Target:** Week 5

### Tasks

#### 4.5.1 Pre-commit Hooks Enhancement ⚪ NOT STARTED
**Description:** Enhance pre-commit hooks for all file types  
**Acceptance Criteria:**
- [ ] Add yamllint for YAML files (.yml, .yaml)
- [ ] Add shellcheck for bash scripts (.sh)
- [ ] Add PSScriptAnalyzer for PowerShell scripts (.ps1)
- [ ] Add markdownlint for Markdown files (.md)
- [ ] Add prettier for JSON/YAML formatting
- [ ] Update `.pre-commit-config.yaml`
- [ ] Document in README.md

**New Hooks:**
```yaml
# .pre-commit-config.yaml additions
- repo: https://github.com/adrienverge/yamllint
  rev: v1.35.1
  hooks:
    - id: yamllint

- repo: https://github.com/shellcheck-py/shellcheck-py
  rev: v0.10.0.1
  hooks:
    - id: shellcheck

- repo: https://github.com/igorshubovych/markdownlint-cli
  rev: v0.41.0
  hooks:
    - id: markdownlint
```

**Dependencies:** None  
**Estimated Time:** 2 hours

---

#### 4.5.2 GitHub Actions Workflow for All Checks ⚪ NOT STARTED
**Description:** Create comprehensive CI workflow for all code quality checks  
**Acceptance Criteria:**
- [ ] Create `.github/workflows/code-quality.yml`
- [ ] Run Python checks (Black, Ruff, mypy)
- [ ] Run YAML checks (yamllint)
- [ ] Run Markdown checks (markdownlint)
- [ ] Run Docker checks (hadolint for Dockerfiles)
- [ ] Run on every push/PR
- [ ] Fail PR if any check fails
- [ ] Add status badge to README.md

**Workflow Structure:**
```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run black --check scripts/python
      - run: uv run ruff check scripts/python
      - run: uv run mypy scripts/python
  
  yaml:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: yamllint .
  
  markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: markdownlint '**/*.md'
  
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: dockerfile/*.Dockerfile
```

**Dependencies:** 4.5.1  
**Estimated Time:** 3 hours

---

#### 4.5.3 Automated Dependency Updates ⚪ NOT STARTED
**Description:** Setup Dependabot for automated dependency PRs  
**Acceptance Criteria:**
- [ ] Create `.github/dependabot.yml`
- [ ] Enable updates for Python (pyproject.toml)
- [ ] Enable updates for Node.js (package.json)
- [ ] Enable updates for Docker (Dockerfile)
- [ ] Enable updates for GitHub Actions
- [ ] Schedule: weekly
- [ ] Auto-merge minor/patch updates (optional)
- [ ] Document in README.md

**Dependabot Config:**
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
  
  - package-ecosystem: "npm"
    directory: "/api"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "npm"
    directory: "/web-content"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "docker"
    directory: "/dockerfile"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Dependencies:** None  
**Estimated Time:** 1 hour

---

## 🎨 Phase 4.6: Web Dashboard Enhancements (Medium Priority)

**Goal:** Implement future enhancements from REFACTOR-SUMMARY.md  
**Priority:** 🟢 MEDIUM  
**Target:** Week 6 (Optional)

### From web-content/REFACTOR-SUMMARY.md:299

**Potential Improvements:**
1. Layer-specific health checks (different polling intervals per layer)
2. Layer metrics aggregation (per-layer resource stats)
3. Visual layer grouping (collapsed/expanded sections in UI)
4. Layer dependencies (explicit dependency trees)
5. Layer scaling controls (UI to scale services within a layer)

### Tasks

#### 4.6.1 Layer-Specific Health Checks ⚪ NOT STARTED
**Description:** Customize health check intervals per layer  
**Acceptance Criteria:**
- [ ] Update `useClusterHealth.ts` to support per-layer intervals
- [ ] Configure intervals: Data (60s), Services (30s), Monitoring (45s), Compute (30s), Network (15s)
- [ ] Add layer health status aggregation
- [ ] Display per-layer health in UI
- [ ] Document in ARCHITECTURE.md

**Rationale:**
- Data layer changes slowly (60s is sufficient)
- Network layer changes frequently (15s for load balancers)
- Reduces API calls by 40%

**Dependencies:** None  
**Estimated Time:** 3 hours

---

#### 4.6.2 Layer Metrics Aggregation ⚪ NOT STARTED
**Description:** Add per-layer resource statistics  
**Acceptance Criteria:**
- [ ] Aggregate CPU/memory/network per layer
- [ ] Add layer metrics endpoint to API (`/api/layers/:id/metrics`)
- [ ] Display layer metrics in dashboard
- [ ] Add layer comparison charts
- [ ] Update ARCHITECTURE.md

**New Metrics:**
- Total CPU usage per layer
- Total memory usage per layer
- Total network I/O per layer
- Service count per layer

**Dependencies:** 4.6.1  
**Estimated Time:** 4 hours

---

#### 4.6.3 Visual Layer Grouping ⚪ NOT STARTED
**Description:** Add collapsible layer sections in UI  
**Acceptance Criteria:**
- [ ] Add expand/collapse buttons to layer sections
- [ ] Save layer collapsed state to localStorage
- [ ] Animate expand/collapse transitions
- [ ] Add "Expand All" / "Collapse All" buttons
- [ ] Update ARCHITECTURE.md

**UI Changes:**
- Layer header becomes clickable
- Chevron icon indicates collapsed/expanded state
- Smooth CSS transitions
- Persist state across page reloads

**Dependencies:** None  
**Estimated Time:** 3 hours

---

#### 4.6.4 Layer Dependencies Visualization ⚪ NOT STARTED
**Description:** Show explicit dependency trees between layers  
**Acceptance Criteria:**
- [ ] Define layer dependencies in config
- [ ] Create dependency graph component
- [ ] Visualize with D3.js or Cytoscape
- [ ] Highlight dependency paths on hover
- [ ] Add to Architecture page
- [ ] Document in ARCHITECTURE.md

**Dependencies:**
```
Network (nginx, loadbalancer)
  ↓
Services (api, web-content)
  ↓
Data (postgres, redis)
  ↓
Monitoring (grafana, prometheus)
```

**Dependencies:** None  
**Estimated Time:** 6 hours

---

#### 4.6.5 Layer Scaling Controls ⚪ NOT STARTED
**Description:** Add UI controls to scale services  
**Acceptance Criteria:**
- [ ] Add scale buttons (+/-) to each service card
- [ ] Call Docker API to scale services
- [ ] Show current replica count
- [ ] Disable for non-scalable services
- [ ] Add scale limits (min: 1, max: 10)
- [ ] Update ARCHITECTURE.md

**API Endpoint:**
```javascript
// POST /api/services/:id/scale
{
  "replicas": 3
}
```

**UI Changes:**
- Scale controls on service cards
- Current replica count badge
- Confirmation dialog for scaling

**Dependencies:** 4.2.1 (requires authentication)  
**Estimated Time:** 5 hours

---

## 📋 Backlog (Low Priority / Future)

**Not planned for v4.0, but documented for future iterations**

### Infrastructure
- [ ] Kubernetes migration guide
- [ ] Terraform configurations for cloud deployment
- [ ] Ansible playbooks for server provisioning
- [ ] Docker Swarm mode support

### Monitoring Enhancements
- [ ] Custom Grafana dashboards per layer
- [ ] Alert rules for service failures
- [ ] Log aggregation with Loki
- [ ] Distributed tracing with Jaeger

### Development Experience
- [ ] Dev containers for all services
- [ ] Hot reload for all services
- [ ] Debugging guides for each language
- [ ] VS Code workspace settings

### Documentation
- [ ] Video tutorials for setup
- [ ] Interactive API documentation (Swagger/OpenAPI)
- [ ] Troubleshooting flowcharts
- [ ] Performance tuning guide

---

## 📊 Progress Tracking

### Velocity Metrics

| Phase | Tasks | Estimated Hours | Completed | In Progress | Not Started |
|-------|-------|-----------------|-----------|-------------|-------------|
| 4.1 Testing | 6 | 13h | 0 | 0 | 6 |
| 4.2 Security | 6 | 18h | 0 | 0 | 6 |
| 4.3 Scripts | 6 | 18h | 0 | 0 | 6 |
| 4.4 Docs | 4 | 11h | 0 | 0 | 4 |
| 4.5 Automation | 3 | 6h | 0 | 0 | 3 |
| 4.6 Dashboard | 5 | 21h | 0 | 0 | 5 |
| **TOTAL** | **30** | **87h** | **0** | **0** | **30** |

### Timeline

**Week 1:** Phase 4.1 - Testing Infrastructure (13h)  
**Week 2:** Phase 4.2 - Security Hardening (18h)  
**Week 3:** Phase 4.3 - Planned Scripts (18h)  
**Week 4:** Phase 4.4 - Documentation (11h)  
**Week 5:** Phase 4.5 - Code Quality (6h)  
**Week 6:** Phase 4.6 - Dashboard Enhancements (21h) - *Optional*

**Total Estimated Duration:** 6 weeks (87 hours)

---

## ✅ Completed Work

### v3.1.0 - Documentation & Python 3.14 Compliance (2025-10-25)

**Completed:**
- ✅ Created scripts/MIGRATION.md (400+ lines)
- ✅ Created scripts/python/audit/README.md (300+ lines)
- ✅ Created scripts/python/utils/README.md (400+ lines)
- ✅ Created scripts/python/validation/README.md (350+ lines)
- ✅ Refactored scripts/python/README.md to overview
- ✅ Updated all Python files with PEP 585 built-in generics
- ✅ Deleted scripts/python/PYTHON-314-COMPLIANCE.md
- ✅ Updated TODO.md to v3.1.0 COMPLETE status
- ✅ Git commit: fed8689 (17 files, 2337 insertions, 209 deletions)
- ✅ Archived TODO-v3.1-20251025.md

**Details:** See `.github/archive/TODO-v3.1-20251025.md` for full v3.1.0 completion

### v3.0 - Scripts Reorganization (2025-10-25)

**Completed:**
- ✅ Reorganized scripts into powershell/, bash/, python/ subdirectories
- ✅ Created orchestrators: orchestrator.ps1, orchestrator.py, orchestrator.sh
- ✅ Extracted Colors class to scripts/python/utils/colors.py (DRY principle)
- ✅ Created comprehensive READMEs for each script category
- ✅ Maintained backward compatibility with root scripts

**Details:** See `.github/archive/TODO-v3.0-20251025.md` (if exists)

### v2.0 - Web Dashboard Refactor (2025-10-24)

**Completed:**
- ✅ Refactored web-content services into 5 architectural layers
- ✅ Created modular layer structure (data, services, monitoring, compute, network)
- ✅ Generated 900+ lines of comprehensive documentation
- ✅ Aligned dashboard with docker-compose.yml cluster structure
- ✅ Zero breaking changes (internal refactor)

**Details:** See `.github/archive/TODO-v2.0-20251025.md`

---

## 🚀 Getting Started with v4.0

**Priority Order:**

1. **Critical (Start Immediately):**
   - Phase 4.1: Testing Infrastructure
   - Phase 4.2: Security Hardening

2. **High Priority (Week 3-4):**
   - Phase 4.3: Planned Scripts
   - Phase 4.4: Documentation Consolidation

3. **Medium Priority (Week 5-6):**
   - Phase 4.5: Code Quality Automation
   - Phase 4.6: Dashboard Enhancements (optional)

**Next Steps:**
1. Review this TODO with team/stakeholders
2. Start with Phase 4.1.1 (Setup pytest)
3. Work through tasks sequentially within each phase
4. Update task status as you complete work
5. Commit progress regularly

---

**Ready to make this platform production-ready! 🎯**
