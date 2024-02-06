import datetime
from flask import Flask, render_template, redirect, url_for, session, request
import config
from werkzeug.middleware.proxy_fix import ProxyFix
from auth.views import auth_bp
from bonus_content.views import bonus_content_bp
from search.views import search_bp
from content.views import content_bp
from content.services.content_service import ContentService
from models.error_model import ErrorModel


# log app start
print(f"APP START TIME: {datetime.datetime.now()}")

app = Flask(__name__)

# for creating fully qualified URLs
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# set up app variables
config.set_app_config(app)

# register blueprints
app.register_blueprint(auth_bp, url_prefix='/a')
app.register_blueprint(bonus_content_bp, url_prefix='/b')
app.register_blueprint(search_bp, url_prefix='/s')
app.register_blueprint(content_bp, url_prefix='/c')

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    print(f"404 error: {e}")
    error_model = ErrorModel("Resource not found", "The requested content was not found.")
    return render_template('error.html', model=error_model), 404

@app.errorhandler(500)
def error(e):
    print(f"500 error: {e}")
    error_model = ErrorModel("An error occurred", "Please wait a moment and try your request again.")
    return render_template('error.html', model=error_model), 500

@app.context_processor
def inject_nav_model(): 
    """
    Injects the user information into the context dictionary.
    'user' dictionary will be available in all templates when logged in.

    Returns:
        dict: 'user' and 'playlists' keys. 
        'user' is the current user, 
        'playlists' is a list of all playlists in the system.
    """
    model = {}
    
    # add the current user to the model
    if "user" in session:
        model["user"] = session["user"]
    else:
        model["user"] = None
        
    content_service = ContentService()
    playlists = content_service.get_playlists()
    
    playlists = sorted(playlists, key=lambda x: x['short_name'])
    
    model["playlists"] = playlists
        
    return dict(nav_model=model)

if __name__ == '__main__':
    app.run( \
        debug=app.config["FLASK_DEBUG"], \
        port=app.config["FLASK_PORT"] \
    )