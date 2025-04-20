import json
from typing import Dict, List, Any
from langchain_openai import AzureChatOpenAI
import os

# Import models from the models directory
from app.models.organizer_models import OrganizerInput, OrganizerOutput
from app.core.langchain_setup import create_simple_chain, get_llm
from app.services.CommonService import read_prompt_template


class OrganizerTool():
    """Tool for organizing and categorizing research content."""
    def __init__(self):
        """
        Initialize the organizer tool with Azure OpenAI credentials from environment variables.
        """
        self.llm = get_llm(0.3)

    def extract_tags(self, oInput:str):
        
        prompt_path="tools/organizer_tool/tag_prompt.txt"
        prompt_template = read_prompt_template(prompt_path)
        # Create the chain
        chain = create_simple_chain(prompt_template, 0.3)
        
        # Run the chain
        result = chain.invoke({"text": oInput})
        result = result.content
        
        # Extract the JSON part (remove the markdown code block markers)
        json_content = result.strip().replace('```json', '').replace('```', '').strip()
        # Parse the JSON string into a Python list
        tags_list = json.loads(json_content)
        # Access the content property of the AIMessage object
        return tags_list
     
    
    def determine_category(self, oInput:str, categories: List[str],path):
        prompt_path = path
        prompt_template = read_prompt_template(prompt_path)
        # Create the chain
        chain = create_simple_chain(prompt_template, 0.3)
        # Run the chain
        result = chain.invoke({"text": oInput, "categories": categories})
        result = result.content

        """Determine the most appropriate category for the content."""
        # Implementation details
        return result