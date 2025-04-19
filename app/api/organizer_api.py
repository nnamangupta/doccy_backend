from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.organizer_models import OrganizerInput, OrganizerOutput
from app.agents.organizer_tool.organizer import OrganizerTool  # Adjusted import path

router = APIRouter(
    prefix="/api/organizer",
    tags=["organizer"],
    responses={404: {"description": "Not found"}},
)

# Dependency to get the organizer tool instance
def get_organizer_tool():
    return OrganizerTool()


@router.post("/analyze", response_model=OrganizerOutput)
async def analyze_content(
    input_data: OrganizerInput,
    organizer: OrganizerTool = Depends(get_organizer_tool)
):
    """
    Analyze research content to extract tags and determine category.
    
    Returns:
        OrganizerOutput: Contains tags, category, and other metadata
    """
    try:
        # Extract tags from the content
        tags = organizer.extract_tags(input_data.text)
        
        # Determine the category
        category = organizer.determine_category(input_data.text, tags)
        
        # Return the organized data
        return OrganizerOutput(
            tags=tags,
            category=category,
            summary=None,  # You can add logic to generate a summary
            related_topics=None  # You can add logic to suggest related topics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for the organizer API."""
    return {"status": "healthy"}