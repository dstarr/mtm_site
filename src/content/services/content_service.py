from flask import current_app, make_response
from datetime import datetime
import pymongo


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
            {
                "name": "playlists"
            },
            {
                "playlists": {"$elemMatch": {"id": id}}
            }
        )

        if playlist is None:
            return None

        return playlist["playlists"][0]

    def get_playlist_with_content_infos(self, playlist_id):
        metadata_collection, content_collection = self._get_collections()

        filter = {"name": "playlists"}
        projection = { "playlists": {"$elemMatch": {"id": playlist_id}}}

        results = metadata_collection.find_one(filter=filter, projection=projection)
        
        try:
            results = results["playlists"][0]
        except KeyError:
            return None

        playlist = results

        sorted_playlist_content = sorted(playlist["content"], key=lambda x: x['display_order'])

        content_infos = []
        for content_pointer in sorted_playlist_content:
            content_info = self._get_content_info(content_pointer["id"], content_collection)
            if content_info["is_active"] == True:
                content_infos.append(content_info)

        playlist["content"] = content_infos
        return playlist

    def get_most_recent_content(self, num_results):
        _, content_collection = self._get_collections()

        items = content_collection \
            .find({}, {'id': 1, 'title': 1, 'date_created': 1}) \
            .sort('date_created', 1) \
            .limit(num_results)

        return items

    def _get_content_info(self, content_id, content_collection):
        
        filter = {"id": content_id}
        projection = { "id": 1, "title": 1, "is_active": 1}
        
        content = content_collection.find_one(filter, projection)

        return content


    def _get_collections(self):

        client = pymongo.MongoClient(
            self._config["COSMOS_DB_CONNECTION_STRING"])
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
