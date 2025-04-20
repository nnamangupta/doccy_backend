from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field

class DataStoreInput(BaseModel):
    """Input for data store operations."""
    operation: str = Field(..., description="Operation to perform: 'store', 'retrieve', 'list', or 'delete'")
    container_name: str = Field(..., description="Name of the data store container to use")
    data_id: Optional[str] = Field(None, description="Unique identifier for the data (required for store, retrieve, delete)")
    data: Optional[Dict[str, Any]] = Field(None, description="Data to store (required for store operation)")
    prefix: Optional[str] = Field(None, description="Prefix filter for list operation")

class DataResponse(BaseModel):
    """Response model for data store operations."""
    status: str
    message: Optional[str] = None
    data: Optional[Union[Dict[str, Any], List[str]]] = None

class ChunkMetadata(BaseModel):
    """Metadata associated with document chunks"""
    RId: str  # Resource ID
    ChunkId: str
    Parent_ChunkId: Optional[str]
    Tag: str
    Category: str

class Chunk(BaseModel):
    """Complete chunk data with content and metadata"""
    RId: str
    ChunkId: str
    Next_ChunkId: Optional[str]
    Previous_ChunkId: Optional[str]
    Parent_ChunkId: Optional[str]
    Context: str
    Tag: str
    Categories: List[str]
    Vector_Embeddings: Optional[List[float]]