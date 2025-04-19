from fastapi import FastAPI
from app.api.langchain_routes import router as langchain_router
from app.api.organizer_api import router as organizer_router

app = FastAPI(title="Doccy API")

# Include the LangChain router
app.include_router(langchain_router)
app.include_router(organizer_router, prefix="/api/organizer", tags=["organizer"])

@app.get("/")
async def root():
    return {"message": "Welcome to Doccy API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}