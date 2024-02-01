import os
from dotenv import load_dotenv

load_dotenv()


def _print_env_vars():
    for key, value in os.environ.items():
        print(f"{key}: {value}")

def _confirm_env_vars_set():
    env_vars_set = True

    if os.environ.get("AZURE_TENANT_ID") == None:
        print("AZURE_TENANT_ID is not set")
        env_vars_set = False
        
    if os.environ.get("AZURE_CLIENT_ID") == None:
        print("AZURE_CLIENT_ID is not set")
        env_vars_set = False

    if os.environ.get("AZURE_CLIENT_SECRET") == None:
        print("AZURE_CLIENT_SECRET is not set")
        env_vars_set = False

    if os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME") == None:
        print("COSMOS_DB_METADATA_COLLECTION_NAME is not set")
        env_vars_set = False

    if os.environ.get("BLOB_STORAGE_CONNECTION_STRING") == None:
        print("BLOB_STORAGE_CONNECTION_STRING is not set")
        env_vars_set = False

    if os.environ.get("BLOB_STORAGE_NAME") == None:
        print("BLOB_STORAGE_NAME is not set")
        env_vars_set = False

    if os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SLIDES") == None:
        print("BLOB_STORAGE_CONTAINER_NAME_SLIDES is not set")
        env_vars_set = False

    if os.environ.get("BLOB_STORAGE_CONTAINER_NAME_PDFS") == None:
        print("BLOB_STORAGE_CONTAINER_NAME_PDFS is not set")
        env_vars_set = False

    if os.environ.get("BLOB_STORAGE_CONTAINER_NAME_VIDEO") == None:
        print("BLOB_STORAGE_CONTAINER_NAME_VIDEO is not set")
        env_vars_set = False

    if os.environ.get("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS") == None:
        print("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS is not set")
        env_vars_set = False
        
    if os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE") == None:
        print("BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE is not set")
        env_vars_set = False
    
    if os.environ.get("COSMOS_DB_CONNECTION_STRING") == None:
        print("COSMOS_DB_CONNECTION_STRING is not set")
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
        
    if env_vars_set == False:
        print("Exiting due to missing environment variables")
        exit(1)

    
def set_app_config(app):
    
    _confirm_env_vars_set()
    
    AZURE_TENANT_ID=os.environ.get("AZURE_TENANT_ID")
    AZURE_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    
    # MSAL configuration
    app.config["MSAL_AUTHORIZE_ENDPOINT"] = f"{AZURE_AUTHORITY}/oauth2/v2.0/authorize"
    app.config["MSAL_CLIENT_ID"] = os.environ.get("AZURE_CLIENT_ID")
    app.config["MSAL_CLIENT_SECRET"] = os.environ.get("AZURE_CLIENT_SECRET")
    app.config["MSAL_SCOPE"] = ["User.Read"]
    app.config["MSAL_TOKEN_ENDPOINT"] = f"{AZURE_AUTHORITY}/oauth2/v2.0/token"

    # azure integration
    app.config["AZURE_AUTHORITY"]=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    app.config["AZURE_CLIENT_ID"]=os.environ.get("AZURE_CLIENT_ID")
    app.config["AZURE_CLIENT_SECRET"]=os.environ.get("AZURE_CLIENT_SECRET")
    app.config["AZURE_ENDPOINT"] = 'https://graph.microsoft.com/v1.0/users'
    app.config["AZURE_REDIRECT_PATH"] = "/content/"
    app.config["AZURE_SCOPE"] = ["User.Read"]
    app.config["AZURE_TENANT_ID"]=AZURE_TENANT_ID

    # cosmos db integration for content
    app.config["COSMOS_DB_CONNECTION_STRING"] = os.environ.get("COSMOS_DB_CONNECTION_STRING")
    app.config["COSMOS_DB_CONTENT_COLLECTION_NAME"] = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
    app.config["COSMOS_DB_METADATA_COLLECTION_NAME"] = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")
    app.config["COSMOS_DB_NAME"] = os.environ.get("COSMOS_DB_NAME")

    # blob storage integration for files
    app.config["BLOB_STORAGE_CONNECTION_STRING"]=os.environ.get("BLOB_STORAGE_CONNECTION_STRING")
    app.config["BLOB_STORAGE_CONTAINER_NAME_OTHER"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OTHER")
    app.config["BLOB_STORAGE_CONTAINER_NAME_PDFS"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_PDFS")
    app.config["BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE")
    app.config["BLOB_STORAGE_CONTAINER_NAME_SLIDES"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SLIDES")
    app.config["BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS")
    app.config["BLOB_STORAGE_CONTAINER_NAME_VIDEO"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_VIDEO")
    app.config["BLOB_STORAGE_NAME"]=os.environ.get("BLOB_STORAGE_NAME")
    # Flask environment
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SESSION_SECRET")
    app.config["FLASK_DEBUG"] = int(os.environ.get("FLASK_DEBUG", 1))
    app.config["FLASK_PORT"] = int(os.environ.get("FLASK_PORT", 5000))
    app.config["FLASK_SESSION_SECRET"] = os.environ.get("FLASK_SESSION_SECRET")
