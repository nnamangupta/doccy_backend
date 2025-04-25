from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.enrich_models import EnrichInput, EnrichOutput
from app.tools.enrich_data.enrich_data import EnrichTool  # Adjusted import path

router = APIRouter(
    prefix="/api/enrich",
    tags=["Enrich"],
    responses={404: {"description": "Not found"}},
)

# Dependency to get the enrich tool instance
def get_enrich_tool():
    return EnrichTool()


@router.post("/enrich", response_model=EnrichOutput)
async def enrich_content(
    input_data: EnrichInput,
    enrich: EnrichTool = Depends(get_enrich_tool)
):
    """
    Enrich content to tranform into a new chunk with bullet/chart/image...etc
    
    Returns:
        Str: Contains the enriched data
    """
    try:
        final_data: str = enrich.reStructure(input_data.meta_data, input_data.old_data, input_data.new_data)
        
        return final_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for the organizer API."""
    return {"status": "healthy"}