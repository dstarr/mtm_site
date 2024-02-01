import os
from dotenv import load_dotenv

load_dotenv()

FLASK_DEBUG=os.environ.get("FLASK_DEBUG")
FLASK_PORT=os.environ.get("FLASK_PORT")

if FLASK_DEBUG == None:
    FLASK_DEBUG=1

if FLASK_PORT == None:
    FLASK_PORT=5000    

def _print_env_vars():
    for key, value in os.environ.items():
        print(f'{key}: {value}')

def set_app_config(app):

    # setup session
    app.config['SECRET_KEY'] = os.urandom(16)
    app.secret_key = app.config['SECRET_KEY']
    
    
    AZURE_TENANT_ID=os.environ.get("AZURE_TENANT_ID")
    AZURE_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    
    # MSAL configuration
    app.config["MSAL_AUTHORIZE_ENDPOINT"] = f"{AZURE_AUTHORITY}/oauth2/v2.0/authorize"
    app.config["MSAL_CLIENT_ID"] = os.environ.get("AZURE_CLIENT_ID")
    app.config["MSAL_CLIENT_SECRET"] = os.environ.get("AZURE_CLIENT_SECRET")
    app.config["MSAL_SCOPE"] = ["User.Read"]
    app.config["MSAL_TOKEN_ENDPOINT"] = f"{AZURE_AUTHORITY}/oauth2/v2.0/token"

    # azure integration
    app.config["AZURE_TENANT_ID"]=os.environ.get("AZURE_TENANT_ID")
    app.config["AZURE_CLIENT_ID"]=os.environ.get("AZURE_CLIENT_ID")
    app.config["AZURE_CLIENT_SECRET"]=os.environ.get("AZURE_CLIENT_SECRET")
    app.config["AZURE_AUTHORITY"]=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    app.config["AZURE_REDIRECT_PATH"] = "/content/"
    app.config["AZURE_ENDPOINT"] = 'https://graph.microsoft.com/v1.0/users'
    app.config["AZURE_SCOPE"] = ["User.Read"]

    # cosmos db integration for content
    app.config["COSMOS_DB_CONNECTION_STRING"] = os.environ.get("COSMOS_DB_CONNECTION_STRING")
    app.config["COSMOS_DB_NAME"] = os.environ.get("COSMOS_DB_NAME")
    app.config["COSMOS_DB_CONTENT_COLLECTION_NAME"] = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
    app.config["COSMOS_DB_METADATA_COLLECTION_NAME"] = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")

    # blob storage integration for files
    app.config["BLOB_STORAGE_CONNECTION_STRING"]=os.environ.get("BLOB_STORAGE_CONNECTION_STRING")
    app.config["BLOB_STORAGE_NAME"]=os.environ.get("BLOB_STORAGE_NAME")
    app.config["BLOB_STORAGE_CONTAINER_NAME_SLIDES"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SLIDES")
    app.config["BLOB_STORAGE_CONTAINER_NAME_PDFS"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_PDFS")
    app.config["BLOB_STORAGE_CONTAINER_NAME_VIDEO"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_VIDEO")
    app.config["BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS")
    app.config["BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE")
    app.config["BLOB_STORAGE_CONTAINER_NAME_OTHER"]=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OTHER")