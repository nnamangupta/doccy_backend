from typing import List
from typing_extensions import TypedDict

from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from IPython.display import Image, display
from langgraph.graph import MessagesState, END

from langchain_core.messages import HumanMessage
from app.agents.Documentation.DocumentationAgent import DocumentationAgent
from app.agents.Feedback.FeedbackAgent import FeedbackAgent
from app.agents.Retrieval.RetrievalAgent import RetrievalAgent
from app.services.CommonService import read_prompt_template
from app.core.langchain_setup import get_llm
from dotenv import load_dotenv
from typing import Literal
from langgraph.types import Command

# Load environment variables
load_dotenv()

get_members = Literal["documentAgent", "feedbackAgent", "retrievalAgent", "FINISH"]

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: get_members

class State(MessagesState):
    next: str

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
        self.coreagent = self._agent_builder()
        
        # Display the current state graph for debugging
        agentChart = Image(self.coreagent.get_graph().draw_mermaid_png());
        with open("app/core/coreagent_chart.png", "wb") as f:
            f.write(agentChart.data)  # Save the chart as a PNG file, overriding if it exists
        display(agentChart)

    # def supervisor_node(self, state: State) -> Command[Literal[get_members, "__end__"]]:
    #     response = self.llm.with_structured_output(Router).invoke(state["messages"])
    #     goto = response["next"]
    #     if goto == "FINISH":
    #         goto = END

    #     return Command(goto=goto, update={"next": goto})
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize all available tools for the agent."""

        return [
            # Tool(
            #     name="supervisor",
            #     func=self.supervisor_node,
            #     description=(
            #         "Starter Node for the graph and responsible for Managing a conversation between the following workers: "
            #         f"{['documentAgent', 'feedbackAgent', 'retrievalAgent']}. "
            #         "Given the user request, determines the next worker to act. "
            #         "Each worker performs a task and responds with their results and status. "
            #         "When all tasks are complete, responds with FINISH."
            #     )
            # ),
            Tool(
                name="documentAgent",
                func=self.documentation_agent.process_request,
                description="Handles requests related to documentation."
            ),
            Tool(
                name="feedbackAgent",
                func=self.feedback_agent.process_request,
                description="Handles user feedback and suggestions."
            ),
            Tool(
                name="retrievalAgent",
                func=self.retrieval_agent.process_request,
                description="Handles data retrieval requests from the datastore."
            )
        ]
    
    def _agent_builder(self):
        """Create the agent agent_builder using LangGraph."""
        # guptanaman: at the moment this is triggering the tool but not with the right arguments.
        return create_react_agent(self.llm, tools=self._initialize_tools(), prompt=self.corePromptTemplate)
        
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
    
    def process_request(self, message: str):
        """Process a user request and return the response."""
        
        def print_stream(stream):
            for s in stream:
                message = s["messages"][-1]
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()
        
        humanMessage = HumanMessage(content=message)
        
        print_stream(self.coreagent.stream(humanMessage, stream_mode="values"))
        
        # response = self.coreagent.invoke({"messages": humanMessage})
        # print_stream(response)
        # return result["messages"][-1].content        
        
        # goto = response["next"]
        # if goto == "FINISH":
        #     goto = END

        # return Command(goto=goto, update={"next": goto})