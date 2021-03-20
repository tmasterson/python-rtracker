import pytest
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
        ("items", "location", "message"),
        (
            ("", "", b"1 or more items are required."),
            ("test", "test", b"Item not found in database."),
            ),
        )
def test_checkin_validation(client, items, location, message):
    response = client.post("/checkin", data={"items": items, "location": location})
    assert message in response.data
