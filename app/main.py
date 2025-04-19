from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.CoreAgent import OrchestratorAgent
from app.services.LoggerService import LoggerService
from app.services.RouterService import RouterService
from app.services.DataStoreManager import DataStoreManager

# Configure logging
LoggerService.configure_logger()
logger = LoggerService.get_logger(__name__)

# Global agent instance
agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    # Startup logic
    global agent
    logger.info("Initializing OrchestratorAgent...")
    try:
        DataStoreManager.initialize()  # Initialize the DataStoreManager with the connection string from environment variables
        agent = OrchestratorAgent.get_instance()
        logger.info("OrchestratorAgent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OrchestratorAgent: {str(e)}")
        raise
    
    yield  # This is where the app runs
    
    # Shutdown logic (if needed)
    logger.info("Shutting down application...")

# Pass the lifespan to FastAPI
app = FastAPI(title="Doccy Backend API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up API routes using the service
RouterService.SetupRoutes(app)