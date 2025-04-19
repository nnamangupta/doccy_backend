from azure.storage.blob import BlobServiceClient, ContainerClient
import os
from typing import Dict, Optional

class DataStoreManager:
    """
    Singleton manager for Azure Storage Service operations.
    Initializes at application startup and provides container clients when needed.
    """
    _instance = None
    _initialized = False
    
    def __new__(cls, connection_string=None):
        if cls._instance is None:
            cls._instance = super(DataStoreManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, connection_string=None):
        if not self._initialized:
            self.connection_string = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if not self.connection_string:
                raise ValueError("Connection string is required")
            self.container_clients: Dict[str, ContainerClient] = {}
            self._blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self._initialized = True

    def get_container_client(self, container_name: str) -> ContainerClient:
        """
        Get or create a container client for the specified container.
        
        Args:
            container_name: Name of the container
            
        Returns:
            ContainerClient for the specified container
        """
        if container_name not in self.container_clients:
            self.container_clients[container_name] = self._blob_service_client.get_container_client(container_name)
        return self.container_clients[container_name]
    
    @classmethod
    def initialize(cls, connection_string=None):
        """
        Explicitly initialize the singleton instance at application startup.
        
        Args:
            connection_string: Optional connection string, otherwise uses environment variable
        
        Returns:
            The initialized DataStoreManager instance
        """
        instance = cls(connection_string)
        return instance
    
    @classmethod
    def get_instance(cls):
        """
        Get the initialized instance of DataStoreManager.
        
        Returns:
            The DataStoreManager instance
        
        Raises:
            RuntimeError: If the manager hasn't been initialized yet
        """
        if cls._instance is None or not cls._instance._initialized:
            raise RuntimeError("DataStoreManager hasn't been initialized yet. Call DataStoreManager.initialize() first.")
        return cls._instance