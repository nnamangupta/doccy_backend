import json
from typing import Dict, List, Any
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage, ChatMessage, AIMessage
import os

# Import models from the models directory
from app.models.enrich_models import EnrichInput, EnrichOutput
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
    def reStructure(mData: str, oData: str = None, nData: str = None):
        if nData is None:
            # means that old + meta data is provided to update the old data - Review and feedback
            prompt_path="tools/enrich_data/update_data.txt"
            prompt_template = read_prompt_template(prompt_path)
            # Create the chain
            chain = create_simple_chain(prompt_template, 0.3)
            
            result = chain.invoke({"oData": oData, "mData": mData})
            result = result.content

        elif oData is None:
            # means that new + meta data is provided and the new data does not match and old data - fresh data
            prompt_path="tools/enrich_data/enrich_data.txt"
            prompt_template = read_prompt_template(prompt_path)
            # Create the chain
            chain = create_simple_chain(prompt_template, 0.3)
            
            result = chain.invoke({"mData": mData, "nData": nData})
            result = result.content

        else:
            # means that old + new + meta data is provided and the new data matches some old data - merge
            prompt_path="tools/enrich_data/transform_data.txt"
            prompt_template = read_prompt_template(prompt_path)
            # Create the chain
            chain = create_simple_chain(prompt_template, 0.3)
            
            result = chain.invoke({"oData": oData, "mData": mData, "nData": nData})
            result = result.content
            
        
        # Access the content property of the AIMessage object
        return "Here is the enriched data: " + str(result)  