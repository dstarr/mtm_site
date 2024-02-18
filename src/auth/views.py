import datetime
from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from .services.table_storage_service import TableStorageService


auth_bp = Blueprint(
    "auth", __name__, 
    template_folder="templates", 
    static_folder="static"
)

@auth_bp.route("/signin", methods=["POST"])
def signin():

    company_name = request.form["companyname"]
    company_url = request.form["companyurl"]
    
    # save them to the databasee
    try:
        table_storage_service = TableStorageService()
        table_storage_service.insert_entity(company_name=company_name, company_url=company_url)
    except Exception as e:
        print("Error inserting entity")
        print(e)
        abort(500)
    
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
