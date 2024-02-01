import os
from flask import Flask, render_template, redirect, url_for, session, request
import config
from werkzeug.middleware.proxy_fix import ProxyFix
from auth.views import auth_bp
from search.views import search_bp

app = Flask(__name__)

# for creating fully qualified URLs
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(search_bp, url_prefix='/search')

# set up app variables
config.set_app_config(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.context_processor
def inject_user(): 
    """
    Injects the user information into the context dictionary.
    'user' dictionary will be available in all templates when logged in.

    Returns:
        dict: A dictionary containing the 'user' key and its corresponding value.
    """
    if "user" in session:
        return dict(user=session['user'])
    else:
        return dict(user=None)

if __name__ == '__main__':
    app.run(port=config.FLASK_PORT, debug=config.FLASK_DEBUG)