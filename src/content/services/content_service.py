from flask import current_app, make_response
from datetime import datetime
import pymongo
from content.models.playlist_with_content_info_model import PlaylistWithContentInfoModel


class ContentService:
    def __init__(self):
        self._config = current_app.config

    def get_all_content(self):
        _, content_collection = self._get_collections()

        contents = content_collection.find()

        return contents

    def get_content(self, content_id):
        _, content_collection = self._get_collections()
        content = content_collection.find_one({"id": content_id})

        return content

    def get_playlists_for_content(self, content_id):
        all_playlists = self.get_playlists()

        content_playlists = []

        # if the content is in the playlist, add it to the list
        for playlist in all_playlists:
            for playlist_item in playlist["content"]:
                if playlist_item["id"] == content_id:
                    content_playlists.append(playlist)

        return content_playlists

    def get_playlists(self):
        metadata_collection, _ = self._get_collections()

        playlists = metadata_collection.find_one({"name": "playlists"})

        return playlists["playlists"]

    def get_playlist(self, id):
        metadata_collection, _ = self._get_collections()

        playlist = metadata_collection.find_one(
            {"name": "playlists"}, {"playlists": {"$elemMatch": {"id": id}}}
        )

        if playlist is None:
            return None

        return playlist["playlists"][0]

    def get_playlist_with_content_infos(self, playlist_id):
        metadata_collection, content_collection = self._get_collections()

        # get the right playlist
        filter = {"name": "playlists"}
        projection = {"playlists": {"$elemMatch": {"id": playlist_id}}}
        results = metadata_collection.find_one(filter=filter, projection=projection)

        playlist = results["playlists"][0]
        content_ids = [content["id"] for content in playlist["content"]]
        
        # get the content info for each content id in the playlist
        # and only include the active content
        filter = filter = { 
                    "id": { 
                        "$in": content_ids
                    },
                    "is_active": { "$ne": False }
                }
        projection = { "id": 1, "title": 1, "is_active": 1 }
        content_docs = list(content_collection.find(filter, projection))
             
        # sort the docs to appear in the same order as the content_ids from the playlist
        content_docs.sort(key=lambda x: content_ids.index(x['id']))
             
        model = PlaylistWithContentInfoModel(playlist=playlist, content_infos=content_docs)
        
        return model
                
    def get_most_recent_content(self, num_results):
        _, content_collection = self._get_collections()

        filter = {"is_active": {"$eq": True}}

        items = (
            content_collection.find(filter, {"id": 1, "title": 1, "date_updated": 1})
            .sort("date_updated", -1)
            .limit(num_results)
        )

        return items

    def _get_collections(self):

        client = pymongo.MongoClient(self._config["COSMOS_DB_CONNECTION_STRING"])
        db = client[self._config["COSMOS_DB_NAME"]]

        content_collection = db[self._config["COSMOS_DB_CONTENT_COLLECTION_NAME"]]
        metadata_collection = db[self._config["COSMOS_DB_METADATA_COLLECTION_NAME"]]

        # create the collection if it does not exist
        if db[self._config["COSMOS_DB_CONTENT_COLLECTION_NAME"]] is None:
            content_collection = db.create_collection(
                name=self._config["COSMOS_DB_CONTENT_COLLECTION_NAME"]
            )
        else:
            content_collection = db[self._config["COSMOS_DB_CONTENT_COLLECTION_NAME"]]

        # create the collection if it does not exist
        if db[self._config["COSMOS_DB_METADATA_COLLECTION_NAME"]] is None:
            metadata_collection = db.create_collection(
                name=self._config["COSMOS_DB_METADATA_COLLECTION_NAME"]
            )
        else:
            metadata_collection = db[self._config["COSMOS_DB_METADATA_COLLECTION_NAME"]]

        return metadata_collection, content_collection
