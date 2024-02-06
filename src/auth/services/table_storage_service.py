import datetime
import uuid
from flask import current_app
from azure.data.tables import TableClient, TableServiceClient

class TableStorageService():
    def __init__(self):
        self._config = current_app.config
        
        self.connection_string = self._config["AURE_STORAGE_CONNECTION_STRING"]
        self.table_name = self._config["TABLE_STORAGE_TABLE_NAME"]
        
        self.table_service_client = TableServiceClient.from_connection_string(conn_str=self.connection_string)

    def _create_table(self):
        print("=====================================")
        print("Creating table")
        print(self.table_name)
        print("=====================================")
        self.table_service_client.create_table(self.table_name)

    def insert_entity(self, company_name, company_url):
            
            table_exists = any(table.name == self.table_name for table in self.table_service_client.list_tables())
            if not table_exists:
                self._create_table()
                
            table_client = TableClient.from_connection_string(conn_str=self.connection_string, table_name=self.table_name)
                
            entity = {
                'PartitionKey': self._config["TABLE_STORAGE_PARTITION_KEY"], 
                'RowKey': str(uuid.uuid4()),
                'company_name': company_name, 
                'company_url': company_url,
            }
            
            table_client.create_entity(entity=entity)
