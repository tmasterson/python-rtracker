import os
from flask import current_app
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from rtracker.db import get_db

bp = Blueprint("reports", __name__, url_prefix='/reports')

@bp.route("/view")
def view():
    reports = []
    for root, dirs, files in os.walk(current_app.config["REPORT_PATH"]):
        for file in files:
            report = {"full_path": os.path.join(root, file), "name": file}
            reports.append(report)
    print(reports)
    return render_template("/reports/view.html", reports=reports)
