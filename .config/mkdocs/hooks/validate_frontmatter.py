"""
Enhanced Frontmatter Validation Hook for MkDocs
===============================================

Validates that all markdown files in docs/ have required frontmatter fields
using Pydantic models for comprehensive validation with modern Python 3.14 features.

Usage:
    Add to hooks.yml:
    ```yaml
    hooks:
      - .config/mkdocs/hooks/validate_frontmatter.py
    ```

Environment Variables:
    MKDOCS_STRICT_FRONTMATTER: Set to "false" to only warn (default: true)
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Protocol
from datetime import datetime

import yaml

try:
    from ..schemas.frontmatter import DocFrontmatter, ALLOWED_TAGS
    from pydantic import ValidationError
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    DocFrontmatter = None
    ALLOWED_TAGS = set()
    ValidationError = None


# ============================================================================
# Type Protocols (PEP 544) - No Runtime Dependencies
# ============================================================================


class FileProtocol(Protocol):
    """Protocol for MkDocs file objects."""

    src_path: str


class FilesProtocol(Protocol):
    """Protocol for MkDocs files collection."""

    def __iter__(self) -> Any: ...
    def __len__(self) -> int: ...


# ============================================================================
# Configuration
# ============================================================================

REQUIRED_FIELDS: frozenset[str] = frozenset({"title", "description"})
OPTIONAL_FIELDS: frozenset[str] = frozenset(
    {
        "tags",
        "date",
        "status",
        "author",
        "category",
        "priority",
        "related",
        "version",
        "template",
    }
)
ALL_FIELDS: frozenset[str] = REQUIRED_FIELDS | OPTIONAL_FIELDS

# Date format pattern (YYYY-MM-DD)
DATE_PATTERN: re.Pattern[str] = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Valid enum values
VALID_STATUS: frozenset[str] = frozenset({"draft", "review", "published", "deprecated"})
VALID_PRIORITY: frozenset[str] = frozenset({"high", "medium", "low"})
VALID_CATEGORY: frozenset[str] = frozenset(
    {
        "installation",
        "configuration",
        "user-guide",
        "api",
        "security",
        "testing",
        "production",
        "development",
        "reference",
    }
)
VALID_TEMPLATE: frozenset[str] = frozenset(
    {"guide", "reference", "tutorial", "api-doc", "changelog"}
)

# Files to skip validation (special pages)
SKIP_FILES: frozenset[str] = frozenset({"index.md", "tags.md", "404.md"})


# ============================================================================
# Validation Functions
# ============================================================================


def extract_frontmatter(content: str) -> tuple[dict[str, Any] | None, list[str]]:
    """
    Extract YAML frontmatter from markdown content.

    Args:
        content: Raw markdown file content

    Returns:
        Tuple of (frontmatter dict or None, list of errors)
    """
    # Check for frontmatter delimiters using structural pattern matching
    match content:
        case str(s) if not s.startswith("---\n"):
            return None, ["Missing frontmatter (must start with '---')"]
        case _:
            pass

    # Find closing delimiter
    try:
        end_index = content.index("\n---\n", 4)
    except ValueError:
        return None, ["Malformed frontmatter (missing closing '---')"]

    # Extract YAML content
    yaml_content = content[4:end_index]

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(yaml_content)
        match frontmatter:
            case dict():
                return frontmatter, []
            case _:
                return None, ["Frontmatter must be a YAML mapping (key-value pairs)"]
    except yaml.YAMLError as e:
        return None, [f"Invalid YAML in frontmatter: {e}"]


def validate_field_value(key: str, value: Any) -> list[str]:
    """
    Validate a single frontmatter field using structural pattern matching.

    Args:
        key: Field name
        value: Field value

    Returns:
        List of validation error messages
    """
    errors: list[str] = []

    match (key, value):
        # Title validation
        case ("title", str(v)) if not v.strip():
            errors.append("'title' must be a non-empty string")
        case ("title", str(v)) if len(v) > 100:
            errors.append(f"'title' too long ({len(v)} chars, max 100)")
        case ("title", str(v)) if not v[0].isupper():
            errors.append("'title' should start with an uppercase letter")
        case ("title", _) if not isinstance(value, str):
            errors.append("'title' must be a string")

        # Description validation
        case ("description", str(v)) if not v.strip():
            errors.append("'description' must be a non-empty string")
        case ("description", str(v)) if len(v) < 10:
            errors.append(f"'description' too short ({len(v)} chars, min 10)")
        case ("description", str(v)) if len(v) > 300:
            errors.append(f"'description' too long ({len(v)} chars, max 300)")
        case ("description", _) if not isinstance(value, str):
            errors.append("'description' must be a string")

        # Tags validation
        case ("tags", list() as tags) if not tags:
            errors.append("'tags' list cannot be empty (omit field if no tags)")
        case ("tags", list() as tags):
            for tag in tags:
                if not isinstance(tag, str) or not re.match(r"^[a-z0-9-]+$", tag):
                    errors.append(
                        f"Invalid tag '{tag}' (must be lowercase alphanumeric with hyphens)"
                    )
        case ("tags", _) if not isinstance(value, list):
            errors.append("'tags' must be a list")

        # Date validation
        case ("date", str(v)) if not DATE_PATTERN.match(v):
            errors.append("'date' must be in YYYY-MM-DD format")
        case ("date", _) if not isinstance(value, str):
            errors.append("'date' must be a string")

        # Status validation
        case ("status", str(v)) if v not in VALID_STATUS:
            errors.append(f"'status' must be one of: {', '.join(sorted(VALID_STATUS))}")
        case ("status", _) if not isinstance(value, str):
            errors.append("'status' must be a string")

        # Priority validation
        case ("priority", str(v)) if v not in VALID_PRIORITY:
            errors.append(f"'priority' must be one of: {', '.join(sorted(VALID_PRIORITY))}")
        case ("priority", _) if not isinstance(value, str):
            errors.append("'priority' must be a string")

        # Category validation
        case ("category", str(v)) if v not in VALID_CATEGORY:
            errors.append(f"'category' must be one of: {', '.join(sorted(VALID_CATEGORY))}")
        case ("category", _) if not isinstance(value, str):
            errors.append("'category' must be a string")

        # Template validation
        case ("template", str(v)) if v not in VALID_TEMPLATE:
            errors.append(f"'template' must be one of: {', '.join(sorted(VALID_TEMPLATE))}")
        case ("template", _) if not isinstance(value, str):
            errors.append("'template' must be a string")

        # Related validation
        case ("related", list() as paths):
            for path in paths:
                if not isinstance(path, str) or not path.endswith(".md"):
                    errors.append(f"Invalid related path '{path}' (must end with .md)")
        case ("related", _) if not isinstance(value, list):
            errors.append("'related' must be a list of file paths")

        # Version validation
        case ("version", str(v)) if not re.match(r"^\d+\.\d+(\.\d+)?$", v):
            errors.append("'version' must match semantic versioning (e.g., 1.0.0)")
        case ("version", _) if not isinstance(value, str):
            errors.append("'version' must be a string")

        # Author validation (optional field)
        case ("author", _):
            pass  # No validation needed for author beyond type checking above

    return errors


def validate_frontmatter(frontmatter: dict[str, Any]) -> list[str]:
    """
    Validate frontmatter fields against DocFrontmatter schema.

    Args:
        frontmatter: Parsed frontmatter dictionary

    Returns:
        List of validation error messages
    """
    errors: list[str] = []

    if PYDANTIC_AVAILABLE and DocFrontmatter:
        # Use Pydantic validation
        try:
            # Convert ISO strings back to datetime objects for validation
            if "date_created" in frontmatter and isinstance(frontmatter["date_created"], str):
                try:
                    frontmatter["date_created"] = datetime.fromisoformat(
                        frontmatter["date_created"].replace("Z", "+00:00")
                    )
                except ValueError:
                    errors.append(f"Invalid date_created format: {frontmatter['date_created']}")

            if "last_updated" in frontmatter and isinstance(frontmatter["last_updated"], str):
                try:
                    frontmatter["last_updated"] = datetime.fromisoformat(
                        frontmatter["last_updated"].replace("Z", "+00:00")
                    )
                except ValueError:
                    errors.append(f"Invalid last_updated format: {frontmatter['last_updated']}")

            # Validate with Pydantic
            DocFrontmatter(**frontmatter)

        except ValidationError as e:
            # Parse Pydantic validation errors
            for error in e.errors():
                field = error.get("loc", ["unknown"])[0]
                msg = error.get("msg", str(error))
                errors.append(f"Field '{field}': {msg}")
    else:
        # Fallback validation without Pydantic
        required_fields = {"date_created", "last_updated", "tags", "description"}
        missing = required_fields - frozenset(frontmatter.keys())
        if missing:
            errors.append(f"Missing required fields: {', '.join(sorted(missing))}")

        # Basic validation
        for key, value in frontmatter.items():
            field_errors = validate_field_value(key, value)
            errors.extend(field_errors)

    return errors


def validate_cross_references(frontmatter: dict[str, Any], docs_dir: Path) -> list[str]:
    """
    Validate cross-references in frontmatter (e.g., related files exist).

    Args:
        frontmatter: Parsed frontmatter dictionary
        file_path: Path to current file
        docs_dir: Root documentation directory

    Returns:
        List of validation error messages
    """
    errors: list[str] = []

    # Validate related files exist
    if "related" in frontmatter and isinstance(frontmatter["related"], list):
        for related_path in frontmatter["related"]:
            if not isinstance(related_path, str):
                continue

            # Convert relative path to absolute
            full_path = docs_dir / related_path
            if not full_path.exists():
                errors.append(f"Related file does not exist: {related_path}")
            elif not full_path.is_file():
                errors.append(f"Related path is not a file: {related_path}")

    # Validate tags are in allowed list (if Pydantic is available)
    if PYDANTIC_AVAILABLE and ALLOWED_TAGS and "tags" in frontmatter:
        if isinstance(frontmatter["tags"], list):
            invalid_tags = set(frontmatter["tags"]) - ALLOWED_TAGS
            if invalid_tags:
                errors.append(
                    f"Invalid tags (not in allowed list): {', '.join(sorted(invalid_tags))}"
                )

    return errors


def validate_content_consistency(frontmatter: dict[str, Any], content: str) -> list[str]:
    """
    Validate consistency between frontmatter and document content.

    Args:
        frontmatter: Parsed frontmatter dictionary
        content: Full document content

    Returns:
        List of validation error messages
    """
    errors: list[str] = []

    # Check if title in frontmatter matches first H1 in content
    if "title" in frontmatter:
        title = frontmatter["title"]
        # Find first H1 heading
        h1_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if h1_match:
            content_title = h1_match.group(1).strip()
            if title != content_title:
                errors.append(f"Title mismatch: frontmatter='{title}' vs content='{content_title}'")

        # Check if description is reflected in content (first paragraph)
    if "description" in frontmatter:
        description = frontmatter["description"].lower()
        # Extract first paragraph after frontmatter
        lines = content.split("\n")
        in_frontmatter = True
        first_paragraph: list[str] = []

        for line in lines:
            if in_frontmatter:
                if line.strip() == "---" and not first_paragraph:
                    continue
                elif line.strip() == "---":
                    in_frontmatter = False
                continue

            if line.strip():
                # Skip headings
                if not line.startswith("#"):
                    first_paragraph.append(line.strip())
            elif first_paragraph:
                break

        if first_paragraph:
            content_start = " ".join(first_paragraph).lower()
            # Check if key words from description appear in first paragraph
            desc_words = set(re.findall(r"\b\w+\b", description))
            content_words = set(re.findall(r"\b\w+\b", content_start))

            # Require at least 30% word overlap for consistency
            if desc_words and len(desc_words & content_words) / len(desc_words) < 0.3:
                errors.append("Description doesn't seem to match document content")

    return errors


# ============================================================================
# Standalone Validation Function
# ============================================================================


def validate_file_frontmatter(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validate frontmatter in a single file (for use by other tools).

    Args:
        file_path: Path to markdown file

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return False, [f"Error reading file: {e}"]

    # Extract and validate frontmatter
    frontmatter, extract_errors = extract_frontmatter(content)

    if extract_errors:
        return False, extract_errors

    if frontmatter is None:
        return False, ["No frontmatter found"]

    # Validate fields
    field_errors = validate_frontmatter(frontmatter)

    return len(field_errors) == 0, field_errors


# ============================================================================
# MkDocs Hook
# ============================================================================


def on_files(files: FilesProtocol, config: dict[str, Any]) -> FilesProtocol:
    """
    MkDocs hook that runs during the files collection phase.
    Validates frontmatter for all markdown files.

    Args:
        files: Collection of files being processed
        config: MkDocs configuration

    Returns:
        Unmodified files collection

    Raises:
        SystemExit: If validation fails and strict mode is enabled
    """
    strict_mode = os.getenv("MKDOCS_STRICT_FRONTMATTER", "true").lower() != "false"

    docs_dir = Path(config["docs_dir"])
    validation_errors: dict[str, list[str]] = {}
    skipped_count = 0

    # Validate each markdown file
    for file in files:
        if not file.src_path.endswith(".md"):
            continue

        # Skip special files
        if Path(file.src_path).name in SKIP_FILES:
            skipped_count += 1
            continue

        # Read file content
        file_path = docs_dir / file.src_path
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as e:
            validation_errors[file.src_path] = [f"Failed to read file: {e}"]
            continue

        # Extract and validate frontmatter
        frontmatter, extract_errors = extract_frontmatter(content)

        if extract_errors:
            validation_errors[file.src_path] = extract_errors
            continue

        if frontmatter is None:
            validation_errors[file.src_path] = ["No frontmatter found"]
            continue

        # Validate fields
        field_errors = validate_frontmatter(frontmatter)

        # Enhanced validation: cross-references and content consistency
        cross_ref_errors = validate_cross_references(frontmatter, docs_dir)
        consistency_errors = validate_content_consistency(frontmatter, content)

        all_errors = field_errors + cross_ref_errors + consistency_errors
        if all_errors:
            validation_errors[file.src_path] = all_errors

    # Report results
    if validation_errors:
        print("\n" + "=" * 80)
        print("FRONTMATTER VALIDATION ERRORS")
        print("=" * 80)
        print(f"Found {len(validation_errors)} file(s) with validation errors:\n")

        for file_path, errors in sorted(validation_errors.items()):
            print(f"❌ {file_path}")
            for error in errors:
                print(f"   - {error}")
            print()

        print("=" * 80)
        print(f"Validated: {len(files) - skipped_count} files")
        print(f"Skipped: {skipped_count} files")
        print(f"Errors: {len(validation_errors)} files")
        print("=" * 80)

        if strict_mode:
            print("\n❌ Build failed due to frontmatter validation errors.")
            print("Set MKDOCS_STRICT_FRONTMATTER=false to only warn.\n")
            sys.exit(1)
        else:
            print("\n⚠️  Warning: Frontmatter validation errors found (non-strict mode).\n")

    else:
        print(f"✅ Frontmatter validation passed ({len(files) - skipped_count} files checked)")

    return files
