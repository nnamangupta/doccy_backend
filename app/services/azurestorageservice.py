import os
from typing import Optional, BinaryIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from app.services.DataStoreManager import DataStoreManager

class AzureStorageService:
    """Service for interacting with Azure Blob Storage."""
    
    @staticmethod
    def upload_file(container_name: str, blob_name: str, file_path: str) -> BlobClient:
        """
        Upload a file to an Azure Storage container.
        
        Args:
            container_name: Name of the target container
            blob_name: Name to assign to the blob in storage
            file_path: Path to the local file to upload
            
        Returns:
            BlobClient for the uploaded blob
        """
        manager = DataStoreManager.get_instance()
        container_client = manager.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        return blob_client
    
    @staticmethod
    def upload_data(container_name: str, blob_name: str, data: BinaryIO) -> BlobClient:
        """
        Upload binary data to an Azure Storage container.
        
        Args:
            container_name: Name of the target container
            blob_name: Name to assign to the blob in storage
            data: Binary data to upload
            
        Returns:
            BlobClient for the uploaded blob
        """
        manager = DataStoreManager.get_instance()
        container_client = manager.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.upload_blob(data, overwrite=True)
        return blob_client
    
    @staticmethod
    def download_data(container_name: str, blob_name: str) -> bytes:
        """
        Download a blob as binary data.
        
        Args:
            container_name: Name of the container
            blob_name: Name of the blob to download
            
        Returns:
            The blob content as bytes
        """
        manager = DataStoreManager.get_instance()
        container_client = manager.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        return blob_client.download_blob().readall()
    
    @staticmethod
    def list_blobs(container_name: str, name_starts_with: Optional[str] = None):
        """
        List all blobs in a container, optionally filtered by prefix.
        
        Args:
            container_name: Name of the container
            name_starts_with: Optional prefix filter
            
        Returns:
            Generator yielding blob items
        """
        manager = DataStoreManager.get_instance()
        container_client = manager.get_container_client(container_name)
        return container_client.list_blobs(name_starts_with=name_starts_with)
    
    @staticmethod
    def delete_blob(container_name: str, blob_name: str) -> None:
        """
        Delete a blob.
        
        Args:
            container_name: Name of the container
            blob_name: Name of the blob to delete
        """
        manager = DataStoreManager.get_instance()
        container_client = manager.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.delete_blob()
