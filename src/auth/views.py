import datetime
from flask import Blueprint, redirect, render_template, request, session, url_for
import msal
import config


auth_bp = Blueprint(
    "auth", __name__, 
    template_folder="templates", 
    static_folder="static"
)

@auth_bp.route("/signin", methods=["POST"])
def signin():

    company_name = request.form["companyname"]
    company_url = request.form["companyurl"]
    time_and_date = datetime.datetime.now()
    
    # save them to the database
    
    # set the user session
    session["user"] = {
        "company_name": company_name,
        "company_url": company_url
    }
    
    return redirect(request.referrer)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(request.referrer)
