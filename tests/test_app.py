from pathlib import Path
import sys

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Tennis Club"
    email = "testuser@example.com"

    # Ensure clean state: remove if already present
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200

    # Verify added
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # Remove
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200

    # Verify removed
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]
