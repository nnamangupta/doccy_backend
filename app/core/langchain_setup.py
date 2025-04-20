from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_llm(temp=0.3):
    """Initialize and return the Azure OpenAI Chat LLM."""
    return AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=temp
    )

def create_simple_chain(prompt_template,temp):
    """Create a simple LangChain with the given prompt template using modern syntax."""
    llm = get_llm(temp)
    # Convert to ChatPromptTemplate for chat models
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Modern way to create chains using the | operator
    chain = prompt | llm
    
    # If you need to transform the input before passing to the prompt
    # chain = RunnablePassthrough() | prompt | llm
    
    return chain