from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import datetime

ALLOWED_TAGS = {
    "installation", "configuration", "user-guide", "api", "security", "testing", "production", "development", "reference"
}

class DocFrontmatter(BaseModel):
    """Pydantic model for MkDocs document frontmatter validation."""
    
    title: str = Field(..., description="Document title")
    description: str = Field(..., description="Document description") 
    tags: List[str] = Field(default_factory=list, description="Document tags")
    date: Optional[str] = Field(None, description="Publication date")
    status: Optional[str] = Field(None, description="Document status")
    author: Optional[str] = Field(None, description="Author name")
    category: Optional[str] = Field(None, description="Document category")
    priority: Optional[str] = Field(None, description="Priority level")
    related: List[str] = Field(default_factory=list, description="Related documents")
    version: Optional[str] = Field(None, description="Version number")
    template: Optional[str] = Field(None, description="Template type")
    date_created: Optional[datetime] = Field(None, description="Creation date")
    last_updated: Optional[datetime] = Field(None, description="Last update date")
