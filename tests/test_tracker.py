import pytest
import io
from rtracker.db import get_db

def test_index(client):
    response = client.get("/")
    assert b"Check Out" in response.data
    assert b"Check In" in response.data
    assert b"2 - CORNERS 8120977429  OUR" in response.data
    assert b"turns" in response.data
    assert b"3 -  CORNERS  8120959284  OUR" not in response.data

def test_checkout(client, app):
    assert client.get("/checkout").status_code == 200
    client.post("/checkout", data={"items": "1 - CORNERS  8120977386  OUR\n3 -  CORNERS  8120959284  OUR\n", "location": "turns"})
    with app.app_context():
        db = get_db()
        count = db.execute("select count(*) from items where location = 'turns'").fetchone()[0]
        assert count == 3

def test_checkin(client, app):
    assert client.get("/checkin").status_code == 200
    client.post("checkin", data={"items": "2 - CORNERS 8120977429  OUR"})
    with app.app_context():
        db = get_db()
        item = db.execute("select * from items where location = 'turns'").fetchone()
        assert item is None

@pytest.mark.parametrize(
        ("items", "location", "message"),
        (
            ("", "", b"1 or more items are required."),
            ("test", "", b"location is required."),
            ("test", "test", b"Item not found in database."),
            ),
        )
def test_checkout_validation(client, items, location, message):
    response = client.post("/checkout", data={"items": items, "location": location})
    assert message in response.data

@pytest.mark.parametrize(
        ("items", "message"),
        (
            ("", b"1 or more items are required."),
            ("test", b"Item not found in database."),
            ),
        )
def test_checkin_validation(client, items, message):
    response = client.post("/checkin", data={"items": items})
    assert message in response.data

def test_add(client, app):
    assert client.get("/add").status_code == 200
    client.post("add", data={"items": "5 - CORNERS 8120977429  OUR"})
    with app.app_context():
        db = get_db()
        count = db.execute("select count(*) from items").fetchone()[0]
        assert count == 4

@pytest.mark.parametrize(
        ("items", "message"),
        (
            ("", b"1 or more items are required."),
            ),
        )
def test_add_validation(client, items, message):
    response = client.post("/add", data={"items": items})
    assert message in response.data

def test_import_file(client, app):
    assert client.get("/import_file").status_code == 200
    files = {'file': io.BytesIO(b"test-data\ntest2")}
    params = {name: (f, "mocked_name_{}".format(name)) for 
            name, f in files.items()}
    params['bucket'] = 'test'
    params['keyname'] = 'mocked_name_test'
    params['content_type'] = 'text'
    response = client.post('/import_file', data=params, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        db = get_db()
        count = db.execute("select count(*) from items").fetchone()[0]
        assert count == 5

def test_import_file_validate_filename(client):
    files = {'file': io.BytesIO(b"test-data\ntest2")}
    params = {name: (f, "".format(name)) for 
            name, f in files.items()}
    params['bucket'] = 'test'
    params['keyname'] = ''
    params['content_type'] = 'text'
    response = client.post('/import_file', data=params, content_type='multipart/form-data', follow_redirects=True)
    print(response.data)
    assert b"No file Name." in response.data

def test_import_file_validate_file_empty(client):
    files = {'file': io.BytesIO(b"")}
    params = {name: (f, "mocked_name_{}".format(name)) for 
            name, f in files.items()}
    params['bucket'] = 'test'
    params['keyname'] = 'mocked_name_test'
    params['content_type'] = 'text'
    response = client.post('/import_file', data=params, content_type='multipart/form-data', follow_redirects=True)
    assert b"The file appears to be empty." in response.data
