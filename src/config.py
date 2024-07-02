import os
from dotenv import load_dotenv

load_dotenv()


def _print_env_vars():
    for key, value in os.environ.items():
        print(f"{key}: {value}")

def _confirm_env_vars_set():
    env_vars_set = True

    if os.environ.get("AZURE_STORAGE_CONNECTION_STRING") == None:
        print("AZURE_STORAGE_CONNECTION_STRING is not set")
        env_vars_set = False

    if os.environ.get("CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING") == None:
        print("CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING is not set")
        env_vars_set = False

    if os.environ.get("COSMOS_DB_NAME") == None:
        print("COSMOS_DB_NAME is not set")
        env_vars_set = False

    if os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME") == None:
        print("COSMOS_DB_CONTENT_COLLECTION_NAME is not set")
        env_vars_set = False

    if os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME") == None:
        print("COSMOS_DB_METADATA_COLLECTION_NAME is not set")
        env_vars_set = False
        
    if os.environ.get("FLASK_SESSION_SECRET") == None:
        print("FLASK_SESSION_SECRET is not set")
        env_vars_set = False
        
    if os.environ.get("TABLE_STORAGE_TABLE_NAME") == None:
        print("TABLE_STORAGE_TABLE_NAME is not set")
        env_vars_set = False
    
    if os.environ.get("TABLE_STORAGE_PARTITION_KEY") == None:
        print("TABLE_STORAGE_PARTITION_KEY is not set")
        env_vars_set = False
    
    # if any of the environment variables are not set, exit the application
    if env_vars_set == False:
        print("Exiting due to missing environment variables")
        exit(1)

    
def set_app_config(app):
    
    _confirm_env_vars_set()

    # azure storage integration
    app.config["AZURE_STORAGE_CONNECTION_STRING"]=os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
   
    # cosmos db integration for content
    app.config["CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING"] = os.environ.get("CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING")
    app.config["COSMOS_DB_CONTENT_COLLECTION_NAME"] = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
    app.config["COSMOS_DB_METADATA_COLLECTION_NAME"] = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")
    app.config["COSMOS_DB_NAME"] = os.environ.get("COSMOS_DB_NAME")
    
    # azure table storage
    app.config["TABLE_STORAGE_TABLE_NAME"]=os.environ.get("TABLE_STORAGE_TABLE_NAME")
    app.config["TABLE_STORAGE_PARTITION_KEY"]=os.environ.get("TABLE_STORAGE_PARTITION_KEY")
    
    # Flask environment
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SESSION_SECRET")
    app.config["FLASK_DEBUG"] = int(os.environ.get("FLASK_DEBUG", 1))
    app.config["FLASK_PORT"] = int(os.environ.get("FLASK_PORT", 5000))
    
    # _print_env_vars()
