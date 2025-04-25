import json
from typing import Dict, List, Any
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage, ChatMessage, AIMessage
import os
# Import models from the models directory
from app.core.langchain_setup import create_simple_chain, get_llm
from app.services.CommonService import read_prompt_template


class EnrichTool():
    """Tool for organizing and categorizing research content."""
    def __init__(self):
        """
        Initialize the organizer tool with Azure OpenAI credentials from environment variables.
        """
        self.llm = get_llm(0.3)
    
    @staticmethod 
    def uIntent(uInput: str):
            # means that old + meta data is provided to update the old data - Review and feedback
            prompt_path="tools/user_intent/intent_prompt.txt"
            prompt_template = read_prompt_template(prompt_path)
            # Create the chain
            uInput = "Turn this data into bullets and add visual chart if required. Convert the pdf into text first."
            chain = create_simple_chain(prompt_template, 0.3)
            iData = uInput
            
            result = chain.invoke({"iData": iData})
            result = result.content
        # Access the content property of the AIMessage object
            return str(result)