import uuid
from flask import current_app
from azure.data.tables import TableClient, TableServiceClient

class TableStorageService():
    def __init__(self):
        self._config = current_app.config
        
        self._connection_string = self._config["CUSTOMCONNSTR_AZURE_STORAGE_CONNECTION_STRING"]
        self._table_name = self._config["TABLE_STORAGE_TABLE_NAME"]
        
        self._table_service_client = TableServiceClient.from_connection_string(conn_str=self._connection_string)


    def insert_entity(self, company_name, company_url):

        try:    
            tables = self._table_service_client.list_tables()
            table_exists = any(table.name == self._table_name for table in tables)
            
            if not table_exists:
                print("Creating table " + self._table_name)
                self._table_service_client.create_table(self._table_name)
                
            entity = {
                'PartitionKey': self._config["TABLE_STORAGE_PARTITION_KEY"], 
                'RowKey': str(uuid.uuid4()),
                'company_name': company_name, 
                'company_url': company_url,
            }
            
            table_client = self._table_service_client.get_table_client(self._table_name)
            table_client.create_entity(entity=entity)
        
        except Exception as e:
            print("Error inserting entity in the table storage service")
            raise e

    def _create_table(self):
        print("=====================================")
        print("Creating table")
        print(self._table_name)
        print("=====================================")
        self._table_service_client.create_table(self._table_name)
