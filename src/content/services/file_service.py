from enum import Enum
from azure.storage.blob import BlobServiceClient
import config

class FileType(Enum):
    PDF = {
        "container_name": config["BLOB_STORAGE_CONTAINER_NAME_PDFS"],
        "content_key": "pdf_url",
        "display_name": "PDF",
        "content_type": "pdf"
    }
    SLIDE = {
        "container_name": config["BLOB_STORAGE_CONTAINER_NAME_SLIDES"],
        "content_key": "slides_url",
        "display_name": "Slides",
        "content_type": "slides"
    }
    TRANSCRIPT = {
        "container_name": config["BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS"],
        "content_key": "transcript_url",
        "display_name": "Transcript",
        "content_type": "transcript"
    }
    VIDEO = {
        "container_name": config["BLOB_STORAGE_CONTAINER_NAME_VIDEO"],
        "content_key": "video_url",
        "display_name": "Video",
        "content_type": "video"
    }
    SAMPLE_CODE = {
        "container_name": config["BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE"],
        "content_key": "sample_code_url",
        "display_name": "Sample code",
        "content_type": "sample_code"
    }

    @property
    def pdf(self):
        return self.PDF
    
    @property
    def slide(self):
        return self.SLIDE
    
    @property
    def transcript(self):
        return self.TRANSCRIPT
    
    @property
    def video(self):
        return self.VIDEO
    
    @property
    def sample_code(self):
        return self.SAMPLE_CODE

class FileService():
    
    def __init__(self, config):
        self._config = config
    
    def get_blob_from_storage(self, blob_name, container_name):
        try:
            blob_client = BlobServiceClient \
                .from_connection_string(self._config["BLOB_STORAGE_CONNECTION_STRING"]) \
                .get_blob_client(container_name, blob=blob_name)

            blob_data = blob_client.download_blob().readall()

            return blob_data

        except Exception as ex:
            print('Exception:')
            print(ex)