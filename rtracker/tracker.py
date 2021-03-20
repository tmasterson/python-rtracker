from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from rtracker.db import get_db

bp = Blueprint("tracker", __name__)


@bp.route("/")
def index():
    """Show all equipment checked out."""
    db = get_db()
    items = db.execute("select item_id, location from items where location != ''").fetchall()
    return render_template("tracker/index.html", items=items)

def items_exist(items, db):
    item_list = items.split("\n")
    item_list[:] = [x for x in item_list if x]
    for item in item_list:
        if db.execute("select item_id from items where item_id = :item", {"item": item}).fetchone() is None:
            return False
    return True

def update_db(items, location, db):
    item_list = items.split("\n")
    item_list[:] = [x for x in item_list if x]
    for item in item_list:
        db.execute("update items set location = ? where item_id = ?", (location, item))
    db.commit()

@bp.route("/checkout", methods=("GET", "POST"))
def checkout():
    if request.method == "POST":
        items = request.form['items']
        location = request.form['location']
        db = get_db()
        error = None
        if not items:
            error = "1 or more items are required."
        elif not location:
            error = "location is required."
        elif not items_exist(items, db):
            error = "Item not found in database."
        if error is None:
            update_db(items, location, db)
            return redirect(url_for("tracker.index"))
        flash(error)
    return render_template("tracker/checkout.html")

@bp.route("/checkin", methods=("GET", "POST"))
def checkin():
    if request.method == "POST":
        items = request.form['items']
        location = ""
        db = get_db()
        error = None
        if not items:
            error = "1 or more items are required."
        elif not items_exist(items, db):
            error = "Item not found in database."
        if error is None:
            update_db(items, location, db)
            return redirect(url_for("tracker.index"))
        flash(error)
    return render_template("tracker/checkin.html")
