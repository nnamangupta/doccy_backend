from fastapi import APIRouter, Depends

router = APIRouter(tags=["system"])

@router.get("/")
async def root():
    """Root endpoint providing basic API information."""
    return {"message": "Welcome to Doccy API"}

@router.get("/health")
async def health_check():
    """Check if the service is healthy."""
    # Import here to avoid circular imports
    from app.main import agent
    return {"status": "healthy", "agent_initialized": agent is not None}