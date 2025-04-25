from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class EnrichInput(BaseModel):
    """Input for the research enrichment tool."""
    old_data: Optional[str] = Field(default= None, description="Old data to be transformed")
    new_data: Optional[str] = Field(default=None, description="New data to be updated with old data")
    meta_data: Optional[str] = Field(default=None, description="Additional context about the research")


class EnrichOutput(BaseModel):
    """Output from the research enrichment tool."""
    final_data: List[str] = Field(..., description="List of relevant tags for the content")
   