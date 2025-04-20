from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.organizer_models import OrganizerInput, OrganizerOutput
from app.tools.organizer_tool.organizer import OrganizerTool  # Adjusted import path

router = APIRouter(
    prefix="/api/organizer",
    tags=["organizer"],
    responses={404: {"description": "Not found"}},
)

# Dependency to get the organizer tool instance
def get_organizer_tool():
    return OrganizerTool()


@router.post("/analyze")#, response_model=OrganizerOutput)
async def analyze_content(
    input_data: OrganizerInput,
    organizer: OrganizerTool = Depends(get_organizer_tool)
):
    """
    Analyze research content to extract tags and determine category.
    
    Returns:
        OrganizerOutput: Contains tags, category, and other metadata
    """
    categories = [
        "Artificial Intelligence", "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Reinforcement Learning", "Robotics", "Data Science", "Big Data",
        "Cloud Computing", "Internet of Things", "Blockchain", "Cybersecurity", "Augmented Reality",
        "Virtual Reality", "Quantum Computing", "Edge Computing"
    ]
    try:
        # Extract tags from the content
        tags: List[str]= organizer.extract_tags(input_data.text)
    
        # Determine the category
        category:str = organizer.determine_category(input_data.text, categories, "tools/organizer_tool/category_prompt.txt")
        category2:str = organizer.determine_category(str(tags), categories, "tools/organizer_tool/category_tag_prompt.txt")
        
        # Return the organized data
        # return OrganizerOutput(
            # tags=tags,
            # category=category,
            # summary=None,  # You can add logic to generate a summary
            # related_topics=None  # You can add logic to suggest related topics
        # )
        Output = [tags, category, category2]
        return Output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for the organizer API."""
    return {"status": "healthy"}