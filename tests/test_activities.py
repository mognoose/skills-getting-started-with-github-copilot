def test_get_activities_returns_expected_activity_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    chess_club = activities["Chess Club"]

    assert chess_club["description"]
    assert chess_club["schedule"]
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_reflects_signup_and_unregister(client):
    email = "new.student@mergington.edu"

    signup_response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]

    unregister_response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]
