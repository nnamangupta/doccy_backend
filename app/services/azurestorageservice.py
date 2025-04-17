import os
from typing import Optional, BinaryIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class AzureStorageService:
    """Service for interacting with Azure Blob Storage."""
    
    def __init__(self, connection_string: str):
        """
        Initialize the Azure Storage service.
        
        Args:
            connection_string: Azure Storage connection string
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    def create_container(self, container_name: str) -> ContainerClient:
        """
        Create a new container if it doesn't exist.
        
        Args:
            container_name: Name of the container to create
            
        Returns:
            ContainerClient for the created/existing container
        """
        container_client = self.blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
        return container_client
    
    def upload_file(self, container_name: str, blob_name: str, file_path: str) -> BlobClient:
        """
        Upload a file to an Azure Storage container.
        
        Args:
            container_name: Name of the target container
            blob_name: Name to assign to the blob in storage
            file_path: Path to the local file to upload
            
        Returns:
            BlobClient for the uploaded blob
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        return blob_client
    
    def upload_data(self, container_name: str, blob_name: str, data: BinaryIO) -> BlobClient:
        """
        Upload binary data to an Azure Storage container.
        
        Args:
            container_name: Name of the target container
            blob_name: Name to assign to the blob in storage
            data: Binary data to upload
            
        Returns:
            BlobClient for the uploaded blob
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        blob_client.upload_blob(data, overwrite=True)
        return blob_client
    
    def download_data(self, container_name: str, blob_name: str) -> bytes:
        """
        Download a blob as binary data.
        
        Args:
            container_name: Name of the container
            blob_name: Name of the blob to download
            
        Returns:
            The blob content as bytes
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        return blob_client.download_blob().readall()
    
    def list_blobs(self, container_name: str, name_starts_with: Optional[str] = None):
        """
        List all blobs in a container, optionally filtered by prefix.
        
        Args:
            container_name: Name of the container
            name_starts_with: Optional prefix filter
            
        Returns:
            Generator yielding blob items
        """
        container_client = self.blob_service_client.get_container_client(container_name)
        return container_client.list_blobs(name_starts_with=name_starts_with)
    
    def delete_blob(self, container_name: str, blob_name: str) -> None:
        """
        Delete a blob.
        
        Args:
            container_name: Name of the container
            blob_name: Name of the blob to delete
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        blob_client.delete_blob()