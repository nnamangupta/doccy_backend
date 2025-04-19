from fastapi import FastAPI, APIRouter
from app.services.LoggerService import LoggerService

logger = LoggerService.get_logger(__name__)

class RouterService:
    """Service for managing API routes and routers."""
    
    @staticmethod
    def register_routers(app: FastAPI, routers: list[APIRouter]) -> None:
        """Register multiple routers with the FastAPI application."""
        for router in routers:
            logger.info(f"Registering router with tags: {router.tags}")
            app.include_router(router)
    
    @staticmethod
    def SetupRoutes(app: FastAPI) -> None:
        """Set up all API routes for the application."""
        # Import routers here to avoid circular imports
        from app.api.langchain_routes import router as langchain_router
        from app.api.AgentRoutes import router as agent_router
        from app.api.CommonRoutes import router as common_router
        
        # List of all routers to include
        routers = [
            common_router,
            langchain_router,
            agent_router,
        ]
        
        # Register all routers
        RouterService.register_routers(app, routers)
        
        logger.info("API routes successfully configured")