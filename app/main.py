from fastapi import FastAPI
from app.api.langchain_routes import router as langchain_router

app = FastAPI(title="Doccy API")

# Include the LangChain router
app.include_router(langchain_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Doccy API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}