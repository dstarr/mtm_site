from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound
from content.services.content_service import ContentService

bonus_content_bp = Blueprint(
    "bonus_content", __name__, 
    template_folder="templates",
    static_folder="static",
)

@bonus_content_bp.route('/<page>')
def page(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)
        
