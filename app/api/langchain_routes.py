from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.langchain_setup import create_simple_chain
from app.agents.research_agent import query_research_agent

router = APIRouter(prefix="/langchain", tags=["langchain"])

class QueryRequest(BaseModel):
    query: str

@router.post("/generate")
async def generate_text(request: QueryRequest):
    """Generate text using LangChain based on the provided query."""
    try:
        # Create a simple prompt template
        prompt_template = """
        Answer the following question in a helpful way:
        
        Question: {query}
        
        Answer:
        """
        
        # Create the chain
        chain = create_simple_chain(prompt_template)
        
        # Run the chain
        result = chain.invoke({"query": request.query})
        
        # Access the content property of the AIMessage object
        return {"generated_text": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

@router.post("/research")
async def research(request: QueryRequest):
    """Research a topic using the research agent with web search capabilities."""
    try:
        result = query_research_agent(request.query)
        return {"research_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during research: {str(e)}")