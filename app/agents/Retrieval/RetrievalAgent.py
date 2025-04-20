from typing import List
import logging
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from app.core.langchain_setup import get_llm
from app.services.CommonService import read_prompt_template

from typing import List
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from IPython.display import Image, display

from langchain_core.messages import HumanMessage
from app.services.CommonService import read_prompt_template
from app.core.langchain_setup import get_llm

from typing import Literal
from langgraph.types import Command

logger = logging.getLogger(__name__)



class RetrievalAgent:
    """
    This agent is designed to handle data retrieval from documents.
    """
    
    def __init__(self):
        self.llm = get_llm()
        self.agent_template = read_prompt_template("agents/Retrieval/RetrievalAgentPrompt.txt")
        self.agent = self._agent_builder()

        # Display the current state graph for debugging
        agentChart = Image(self.agent.get_graph().draw_mermaid_png())
        with open("app/agents/Retrieval/retrievalAgent_chart.png", "wb") as f:
            f.write(agentChart.data)  # Save the chart as a PNG file, overriding if it exists
        display(agentChart)
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize all available tools for the agent."""
        
        return [
        ]

    def _agent_builder(self):
        """Create the agent agent_builder using LangGraph."""
        
        return create_react_agent(self.llm, tools=self._initialize_tools(), prompt=self.agent_template)
        
    def process_request(self, user_message: str) -> Command[Literal["coreagent"]]:
        """Process a request from core agent and return the response."""

        def print_stream(stream):
            for s in stream:
                message = s["messages"][-1]
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()

        humanMessage = HumanMessage(content=user_message)
        # print_stream(self.agent.stream(humanMessage, stream_mode="values"))

        result = self.agent.invoke(humanMessage)
        print_stream(result)

        # return Command(goto="coreagent", update={"messages": [result]})
        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name=__name__)
                ]
            },
            goto="coreagent",
        )