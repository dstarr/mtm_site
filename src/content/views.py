from flask import Blueprint, abort, redirect, render_template, current_app, url_for

from models.error_model import ErrorModel

# from .services.file_service import FileService, FileType
from .services.content_service import ContentService
from .models.detail_model import DetailModel

content_bp = Blueprint(
    "content", __name__, 
    template_folder="templates",
    static_folder="static",
)

@content_bp.route('/<content_id>')
def content_detail(content_id):
    with current_app.app_context():
        content_service = ContentService()

        content = content_service.get_content(content_id)
        if content is None:
            abort(404)
        
        content_playlists = content_service.get_playlists_for_content(content_id)
                
        model = DetailModel(content=content, playlists_info=content_playlists)
    
        return render_template('content_detail.html', model=model)
        

@content_bp.route('/p/<playlist_id>')
def playlist(playlist_id):
    with current_app.app_context():
        content_service = ContentService()
        playlist = content_service.get_playlist_with_content_infos(playlist_id=playlist_id)
        if playlist is None:
            abort(404)
        
        return render_template('playlist.html', model=playlist)

@content_bp.route('/log/<num_items>')
def content_log(num_items=10):
    with current_app.app_context():
        content_service = ContentService()
    content_log_items = content_service.get_most_recent_content(int(num_items))
    
    print(content_log_items)
    
    return render_template('content_log.html', model=content_log_items)