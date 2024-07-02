from flask import Blueprint, redirect, render_template, request, url_for, current_app
from search.models.search_results_model import SearchResultsModel
from search.services.search_service import SearchService

# import app

search_bp = Blueprint(
    "search", __name__, 
    template_folder="templates", 
    static_folder="static"
)

@search_bp.before_request
def before_request():
    global cosmos_config
    cosmos_config = {
        "connection_string": current_app.config["COSMOS_DB_CONNECTION_STRING"],
        "db_name": current_app.config["COSMOS_DB_NAME"],
        "content_collection_name": current_app.config["COSMOS_DB_CONTENT_COLLECTION_NAME"],
    }

    global search_service
    search_service = SearchService(cosmos_config=cosmos_config)

@search_bp.route("/", methods=["POST"])
def search_results():
    search_term = request.form["search_term"]
    
    if search_term == "":
        return redirect(url_for("home"))
    
    search_results = search_service.search_content(search_term)
    search_results_model = SearchResultsModel(search_term, search_results)
    
    return render_template("search_index.html", model=search_results_model)