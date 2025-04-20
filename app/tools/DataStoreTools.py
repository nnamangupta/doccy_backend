from typing import Dict, Any, List, Union, Type
from langchain.tools import BaseTool
import json
from dotenv import load_dotenv
from app.services.azurestorageservice import AzureStorageService
from app.models.DataStoreModel import DataStoreInput
from langchain_core.tools import Tool, StructuredTool

# Load environment variables
load_dotenv()

class DataStoreTools(BaseTool):
    """Tool for storing and retrieving data from Azure Blob Storage."""
    name: str = "data_store_tool"
    description: str = """Store, retrieve, list, or delete data from the data store container.
                - Only triggered by other tools to handle data the below actions:
                    - For 'store' action: Provide container_name, data_id, and data
                    - For 'retrieve' action: Provide container_name and data_id
                    - For 'list' action: Provide container_name and optional prefix
                    - For 'delete' action: Provide container_name and data_id"""
    args_schema: Type[DataStoreInput] = DataStoreInput
    
    def __init__(self):
        """Initialize the DataStoreTool with Azure Storage connection."""
        super().__init__()
    
    def _store_data(self, dataStoreInput: DataStoreInput) -> Dict[str, str]:
        """Store data in Azure Blob Storage."""
        if not dataStoreInput.data_id:
            raise ValueError("data_id is required for store operation")
        if not dataStoreInput.data:
            raise ValueError("data is required for store operation")

        json_data = json.dumps(dataStoreInput.data).encode('utf-8')
        from io import BytesIO
        data_stream = BytesIO(json_data)

        blob_name = f"{dataStoreInput.data_id}.json"
        AzureStorageService.upload_data(dataStoreInput.container_name, blob_name, data_stream)

        return {"status": "success", "message": f"Data stored with ID: {dataStoreInput.data_id}"}

    def _retrieve_data(self, dataStoreInput: DataStoreInput) -> Union[Dict[str, Any], Dict[str, str]]:
        """Retrieve data from Azure Blob Storage."""
        if not dataStoreInput.data_id:
            raise ValueError("data_id is required for retrieve operation")

        blob_name = f"{dataStoreInput.data_id}.json"
        try:
            data_bytes = AzureStorageService.download_data(dataStoreInput.container_name, blob_name)
            return json.loads(data_bytes.decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"Failed to retrieve data: {str(e)}"}

    def _list_data(self, dataStoreInput: DataStoreInput) -> Union[List[str], Dict[str, str]]:
        """List data in Azure Blob Storage."""
        try:
            blobs = AzureStorageService.list_blobs(dataStoreInput.container_name, name_starts_with=dataStoreInput.prefix)
            return [blob.name.replace('.json', '') for blob in blobs]
        except Exception as e:
            return {"status": "error", "message": f"Failed to list data: {str(e)}"}

    def _delete_data(self, dataStoreInput: DataStoreInput) -> Dict[str, str]:
        """Delete data from Azure Blob Storage."""
        if not dataStoreInput.data_id:
            raise ValueError("data_id is required for delete operation")

        blob_name = f"{dataStoreInput.data_id}.json"
        try:
            AzureStorageService.delete_blob(dataStoreInput.container_name, blob_name)
            return {"status": "success", "message": f"Data with ID {dataStoreInput.data_id} deleted"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete data: {str(e)}"}

    def _run(self, operation: str, container_name: str, data_id: str = "", data: Dict[str, Any] = None, prefix: str = "") -> Union[Dict[str, Any], List[str], str]:
        """
        Run the data store tool with the specified operation.

        Args:
            operation (str): The operation to perform. Must be one of 'store', 'retrieve', 'list', or 'delete'.
            container_name (str): The name of the Azure Blob Storage container.
            data_id (str, optional): The ID of the data for 'store', 'retrieve', or 'delete' operations. Defaults to an empty string.
            data (str, optional): The data to store for the 'store' operation. Defaults to an empty string.
            prefix (str, optional): The prefix to filter blobs for the 'list' operation. Defaults to an empty string.

        Returns:
            Union[Dict[str, Any], List[str], str]: The result of the operation, which varies based on the operation type.
        """
        operations = {
            "store": self._store_data,
            "retrieve": self._retrieve_data,
            "list": self._list_data,
            "delete": self._delete_data
        }

        dataStoreInput: DataStoreInput = DataStoreInput(
            operation=operation,
            container_name=container_name,
            data_id=data_id,
            data=data,
            prefix=prefix
        )

        if dataStoreInput.operation not in operations:
            raise ValueError(f"Unknown operation: {dataStoreInput.operation}. Must be 'store', 'retrieve', 'list', or 'delete'")

        return operations[dataStoreInput.operation](dataStoreInput)

    async def _arun(self, operation: str, container_name: str, data_id: str = "", data: Dict[str, Any] = None, prefix: str = "") -> Union[Dict[str, Any], List[str], str]:
        """Async implementation of the data store tool."""
        return self._run(operation, container_name, data_id, data, prefix)
