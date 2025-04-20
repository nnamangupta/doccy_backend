from json import tool
from typing import List
from langchain_core.tools import Tool, StructuredTool

from app.services.LoggerService import LoggerService

logger = LoggerService.get_logger(__name__)

# def _get_generate_embeddings() -> StructuredTool:
#         """Get the DataStoreTool for interacting with Azure Blob Storage."""
#         return StructuredTool.from_function(
#             func=_generate_embeddings,
#             name="generate_embeddings",
#             description="Generate vector embeddings for a list of chunks.",
#             )
    

# @tool
# def _generate_embeddings(self, chunks: List[Chunk]) -> None:
#         """Generate vector embeddings for chunks"""
#         if not self.vector_embedding_service:
#             logger.warning("Vector embedding service not configured")
#             return
            
#         for chunk in chunks:
#             chunk.Vector_Embeddings = self.vector_embedding_service.embed(chunk.Context)

