from fastapi import APIRouter, HTTPException, Depends
from app.core.CoreAgent import OrchestratorAgent
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/agent",
    tags=["agent"],
)

def get_agent():
    """Get the orchestrator agent instance."""
    agent = OrchestratorAgent.get_instance()
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return agent

@router.post("/process_query")
async def process_query(query: str, agent: OrchestratorAgent = Depends(get_agent)):
    """Process a user query using the orchestrator agent."""
    try:
        response = agent.process_request(query)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))