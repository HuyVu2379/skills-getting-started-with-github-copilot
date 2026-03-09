def test_root_redirects_to_static_index(client):
    # Arrange
    expected_redirect_path = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect_path


def test_get_activities_returns_expected_payload(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert expected_activity_name in payload
    assert "participants" in payload[expected_activity_name]


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity_name = "Science Club"
    activity_path = "Science%20Club"
    email = "newstudent@mergington.edu"

    existing_participants = client.get("/activities").json()[activity_name]["participants"]
    assert email not in existing_participants

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    updated_participants = client.get("/activities").json()[activity_name]["participants"]
    assert email in updated_participants


def test_signup_for_activity_returns_400_for_duplicate_student(client):
    # Arrange
    activity_path = "Chess%20Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_path}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_for_activity_returns_404_for_missing_activity(client):
    # Arrange
    missing_activity_path = "Nonexistent%20Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{missing_activity_path}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
