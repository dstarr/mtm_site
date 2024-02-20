class PlaylistWithContentInfoModel():

    def __init__(self, playlist, content_infos):
        self._playlist = playlist
        self._content_infos = content_infos
        
    def get_playlist(self):
        return self._playlist
    
    def get_content_infos(self):
        return self._content_infos