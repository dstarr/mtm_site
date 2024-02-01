from flask import Blueprint, redirect, render_template, request, session, url_for
import msal
import config


auth_bp = Blueprint(
    "auth", __name__, 
    template_folder="templates", 
    static_folder="static"
)


# MSAL instance
# msal_app = msal.ConfidentialClientApplication(
#     config["MSAL_CLIENT_ID"],
#     authority=config.AZURE_AUTHORITY,
#     client_credential=config["MSAL_CLIENT_SECRET"]
# )

@auth_bp.route("/login")
def login():
    auth_url = msal.get_authorization_request_url(
        config["MSAL_SCOPE"],
        redirect_uri=url_for("authorized", _external=True)
    )
    return redirect(auth_url)

@auth_bp.route("/authorized")
def authorized():
    result = auth_bp.acquire_token_by_authorization_code(
        request.args["code"],
        scopes=config["MSAL_SCOPE"],
        redirect_uri=url_for("authorized", _external=True)
    )
    if "error" in result:
        return f"Error: {result['error_description']}"

    session["user"] = result.get("id_token_claims")
    
    print(session["user"])
    
    return redirect(url_for("index"))

@auth_bp.route("/logout")
def logout():
    return redirect(url_for("app.index"))

# @auth_bp.before_request
# def check_user_authenticated():
#     if "user" not in session:
#         return redirect(url_for('login'))
