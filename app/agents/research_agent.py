from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
# from langchain_core.messages import AIMessage, HumanMessage
# from langchain_core.tools import Tool
# from langchain.tools import DuckDuckGoSearchRun
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_research_agent():
    """Create a research agent that can search the web for information."""
    
    # Initialize search tool
    # search_tool = DuckDuckGoSearchRun()
    
    tools = [
        # Tool(
        #     name="web_search",
        #     func=search_tool.run,
        #     description="Searches the web for information. Use this for questions about current events, data, or any information you don't know about."
        # )
    ]
    
    # Create Azure OpenAI LLM
    llm = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.7
    )
    
    # Create the prompt with a placeholder for the agent's scratchpad
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful research assistant. 
        You have access to the following tools:
        
        {tools}
        
        Use these tools to best help the user with their questions.
        Always provide helpful, accurate responses and cite your sources when possible.
        """),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"])
        }
        | prompt
        | llm.bind(functions=[tool.metadata for tool in tools])
        | OpenAIFunctionsAgentOutputParser()
    )
    
    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def query_research_agent(query: str):
    """
    Run a query through the research agent.
    
    Args:
        query: The user's question or request
        
    Returns:
        The agent's response
    """
    agent = create_research_agent()
    response = agent.invoke({"input": query})
    return response["output"]