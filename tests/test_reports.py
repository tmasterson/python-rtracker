import pytest
import io
from rtracker.db import get_db
import shutil
import os
from datetime import datetime

def test_reports(client, app):
    test_file = os.path.join(app.config["REPORT_PATH"], "test.txt")
    shutil.copy(os.path.join(os.path.dirname(__file__), "data.sql"), test_file)
    response = client.get("/reports/view")
    assert response.status_code == 200
    assert b"test.txt" in response.data
    os.unlink(test_file)

def test_create(client, app):
    filename = "checkedout-{}.txt".format(datetime.now().strftime("%Y%m%d"))
    response = client.get("/reports/create", follow_redirects=True)
    assert response.status_code == 200
    assert filename.encode("utf-8") in response.data
    with open(os.path.join(app.config["REPORT_PATH"], filename), "r") as f:
        lines = f.read()
    assert '2 - CORNERS 8120977429  OUR,turns' in lines
    os.unlink(os.path.join(app.config["REPORT_PATH"], filename))

def test_create_with_no_data(client, app):
    with app.app_context():
        get_db().execute("update items set location = ''")
        get_db().commit()
    response = client.get("/reports/create", follow_redirects=True)
    assert b"Nothing checked out.  No report generated." in response.data
