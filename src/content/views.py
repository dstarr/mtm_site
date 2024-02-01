from flask import Blueprint, render_template, current_app

# from .services.file_service import FileService, FileType
from .services.content_service import ContentService
from .models.detail_model import DetailModel

content_bp = Blueprint(
    "content", __name__, 
    template_folder="templates",
    static_folder="static",
)

@content_bp.route('/')
def index():
    with current_app.app_context():
        content_service = ContentService()
        content = content_service.get_all_content()
        return render_template('index.html', model=content)

@content_bp.route('/<content_id>')
def content_detail(content_id):
    with current_app.app_context():
        content_service = ContentService()

        content = content_service.get_content(content_id)
        content_playlists = content_service.get_playlists_for_content(content_id)
        
        model = DetailModel(content=content, playlists_info=content_playlists)
        return render_template('content_detail.html', model=model)