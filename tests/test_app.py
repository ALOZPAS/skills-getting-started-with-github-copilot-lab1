import copy
import src.app as app_module
from fastapi.testclient import TestClient
import pytest

client = TestClient(app_module.app)
orig_activities = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # reset in-memory activities before each test
    app_module.activities = copy.deepcopy(orig_activities)
    yield
    app_module.activities = copy.deepcopy(orig_activities)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_appears():
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    data = client.get("/activities").json()
    assert email not in data[activity_name]["participants"]

    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200
    j = resp.json()
    assert "Signed up" in j["message"]

    data = client.get("/activities").json()
    assert email in data[activity_name]["participants"]


def test_remove_participant():
    activity_name = "Chess Club"
    email = "toremove@mergington.edu"

    # sign up first
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200

    data = client.get("/activities").json()
    assert email in data[activity_name]["participants"]

    # delete
    resp = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert resp.status_code == 200

    data = client.get("/activities").json()
    assert email not in data[activity_name]["participants"]


def test_delete_nonexistent_returns_404():
    activity_name = "Chess Club"
    # email not present
    resp = client.delete(f"/activities/{activity_name}/participants?email=noone@mergington.edu")
    assert resp.status_code == 404
