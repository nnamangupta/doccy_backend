from typing import List
from typing_extensions import TypedDict

from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from IPython.display import Image, display
from langgraph.graph import StateGraph, END

from langchain_core.messages import HumanMessage
from app.agents.Documentation.DocumentationAgent import DocumentationAgent
from app.agents.Feedback.FeedbackAgent import FeedbackAgent
from app.agents.Retrieval.RetrievalAgent import RetrievalAgent
from app.models.State import State
from app.services.CommonService import read_prompt_template
from app.core.langchain_setup import get_llm
from dotenv import load_dotenv
from typing import Literal
from langgraph.types import Command

# Load environment variables
load_dotenv()

get_members = Literal["DocumentationAgent", "FeedbackAgent", "RetrievalAgent"]

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: get_members

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
        self.corePromptTemplate = read_prompt_template("core/CoreAgentPromptTemplate.txt")
        self.documentation_agent = DocumentationAgent()
        self.feedback_agent = FeedbackAgent()
        self.retrieval_agent = RetrievalAgent()
        self.graph = self._agent_builder()
        
        # Display the current state graph for debugging
        agentChart = Image(self.graph.get_graph().draw_mermaid_png())
        with open("app/core/coreagent_chart.png", "wb") as f:
            f.write(agentChart.data)  # Save the chart as a PNG file, overriding if it exists
        display(agentChart)

    def coreagent(self, state: State) -> Command[Literal[get_members, "__end__"]]:
        messages = [{"role": "system", "content": self.corePromptTemplate},] + state["messages"]
        response = self.llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})
    
    # def _initialize_tools(self) -> List[Tool]:
    #     """Initialize all available tools for the agent."""

    #     return [
    #         # Tool(
    #         #     name="supervisor",
    #         #     func=self.coreagent,
    #         #     description=(
    #         #         "Starter Node for the graph and responsible for Managing a conversation between the following workers: "
    #         #         f"{['documentAgent', 'feedbackAgent', 'retrievalAgent']}. "
    #         #         "Given the user request, determines the next worker to act. "
    #         #         "Each worker performs a task and responds with their results and status. "
    #         #         "When all tasks are complete, responds with FINISH."
    #         #     )
    #         # ),
    #         Tool(
    #             name="documentAgent",
    #             func=self.documentation_agent.process_request,
    #             description="Handles requests related to documentation."
    #         ),
    #         Tool(
    #             name="feedbackAgent",
    #             func=self.feedback_agent.process_request,
    #             description="Handles user feedback and suggestions."
    #         ),
    #         Tool(
    #             name="retrievalAgent",
    #             func=self.retrieval_agent.process_request,
    #             description="Handles data retrieval requests from the datastore."
    #         )
    #     ]
    
    def _agent_builder(self):
        """Create the agent agent_builder using LangGraph."""
        builder = StateGraph(State)
        builder.set_entry_point("coreagent")
        builder.add_node("coreagent", self.coreagent)
        builder.add_node("DocumentationAgent", self.documentation_agent.process_request)
        builder.add_node("FeedbackAgent", self.feedback_agent.process_request)
        builder.add_node("RetrievalAgent", self.retrieval_agent.process_request)
        return builder.compile()
    
    def process_request(self, message: str):
        """Process a user request and return the response."""
        
        for s in self.graph.stream(
            {"messages": [("user", message)]}, subgraphs=True
        ):
            print(s)
            print("----")