from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unsubscribe_participant_from_activity():
    activity_name = "Chess Club"
    email = "withdrawal-test@mergington.edu"

    # Ensure the test email is not already present before the request.
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    signup = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )
    assert signup.status_code == 200

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    refreshed = client.get("/activities")
    assert refreshed.status_code == 200
    assert email not in refreshed.json()[activity_name]["participants"]
