from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class OrganizerInput(BaseModel):
    """Input for the research organizer tool."""
    text: str = Field(..., description="The research text content to organize and categorize")
    existing_tags: Optional[List[str]] = Field(default=None, description="Existing tags to consider")
    context: Optional[str] = Field(default=None, description="Additional context about the research")


class OrganizerOutput(BaseModel):
    """Output from the research organizer tool."""
    tags: List[str] = Field(..., description="List of relevant tags for the content")
    category: str = Field(..., description="Primary category for the content")
    summary: Optional[str] = Field(default=None, description="Brief summary of the content")
    related_topics: Optional[List[str]] = Field(default=None, description="Potential related research topics")