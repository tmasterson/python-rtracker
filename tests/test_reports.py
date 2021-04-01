import pytest
import io
from rtracker.db import get_db
import shutil
import os

def test_reports(client, app):
    test_file = os.path.join(app.config["REPORT_PATH"], "test.txt")
    shutil.copy(os.path.join(os.path.dirname(__file__), "data.sql"), test_file)
    response = client.get("/reports/view")
    assert response.status_code == 200
    assert b"test.txt" in response.data
    os.unlink(test_file)
