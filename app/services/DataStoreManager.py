from azure.storage.blob import BlobServiceClient, ContainerClient

class DataStoreManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.container_clients = {}

    @staticmethod
    def get_container_client(self, container_name):
        if container_name not in self.container_clients:
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.container_clients[container_name] = blob_service_client.get_container_client(container_name)
        return self.container_clients[container_name]