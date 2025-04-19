from typing import List, TypedDict
from langchain_core.tools import Tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent, ToolNode

from langchain_core.messages import HumanMessage, AIMessage
from app.tools.DataStoreTools import DataStoreTools
from app.core.langchain_setup import get_llm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the state structure
class CoreAgentState(TypedDict):
    messages: list  # Chat history
    tools: list     # Available tools
    next_step: str  # Next action

class OrchestratorAgent:
    """Agent responsible for handling incoming requests and routing them to appropriate tools."""
    
    _instance = None  # Singleton instance
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance of the agent."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize the orchestrator agent."""
        self.llm = get_llm()
        self.tools = self._initialize_tools()
        self.tool_executor = ToolNode(self.tools)
        self.agent = self._agent_builder()
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize all available tools for the agent."""
        data_store_tool = DataStoreTools()
        return [
            Tool(
                name="data_store_tools",
                func=data_store_tool._run,
                description="Store, retrieve, list, or delete data from the data store",
            )
        ]
    
    def _agent_builder(self):
        """Create the agent agent_builder using LangGraph."""
        # guptanaman: at the moment this is triggering the tool but not with the right arguments.
        return create_react_agent(self.llm, tools=self.tools)
        
        # agent_builder = StateGraph(CoreAgentState)
        # def route_request(state):
        #     """Determine the next step based on the user request."""
        #     response = self.llm.invoke(
        #         state["messages"] + [AIMessage(content="I'll help you with that request.")],
        #         tool_choice="required",
        #         tools=[t.to_openai_function() for t in state["tools"]]
        #     )
        #     return "execute_tool" if response.tool_calls else "respond_directly"
        
        # def execute_tool(state):
        #     """Execute the selected tool."""
        #     response = self.llm.invoke(
        #         state["messages"],
        #         tools=[t.to_openai_function() for t in state["tools"]],
        #         tool_choice="required"
        #     )
        #     action = response.tool_calls[0]
        #     tool_output = self.tool_executor.execute_tool(action.name, action.args)
        #     return {
        #         "messages": state["messages"] + [
        #             AIMessage(content=f"I'll use the {action.name} tool."),
        #             AIMessage(content=f"Tool result: {tool_output}")
        #         ],
        #         "next_step": "formulate_response"
        #     }
        
        # def respond_directly(state):
        #     """Generate a direct response without using tools."""
        #     response = self.llm.invoke(state["messages"])
        #     return {
        #         "messages": state["messages"] + [response],
        #         "next_step": END
        #     }
        
        # def formulate_response(state):
        #     """Create a final response based on tool outputs."""
        #     response = self.llm.invoke(
        #         state["messages"] + [AIMessage(content="What's my final response to the user?")]
        #     )
        #     return {
        #         "messages": state["messages"] + [response],
        #         "next_step": END
        #     }
        
        # # Add nodes and edges to the agent_builder
        # agent_builder.add_node("route_request", route_request)
        # agent_builder.add_node("execute_tool", execute_tool)
        # agent_builder.add_node("respond_directly", respond_directly)
        # agent_builder.add_node("formulate_response", formulate_response)
        # agent_builder.add_edge("route_request", "execute_tool")
        # agent_builder.add_edge("route_request", "respond_directly")
        # agent_builder.add_edge("execute_tool", "formulate_response")
        # agent_builder.add_edge("formulate_response", END)
        # agent_builder.add_edge("respond_directly", END)
        # agent_builder.set_entry_point("route_request")

        # return agent_builder.compile()
    
    def process_request(self, user_message: str) -> str:
        """Process a user request and return the response."""
        result = self.agent.invoke({
            "messages": [HumanMessage(content=user_message)],
            # "tools": self.tools,
            # "next_step": "route_request"
        })
        return result["messages"][-1].content
