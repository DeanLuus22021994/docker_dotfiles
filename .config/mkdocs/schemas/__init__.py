"""Pydantic schemas for MkDocs frontmatter validation."""

from .frontmatter import DocFrontmatter, ALLOWED_TAGS

__all__ = ["DocFrontmatter", "ALLOWED_TAGS"]
