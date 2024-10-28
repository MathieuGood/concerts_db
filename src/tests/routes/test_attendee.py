def test_create_attendee(client):
    response = client.post(
        "/attendee/",
        json={
            "firstname": "Graham",
            "lastname": "Chapman",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["firstname"] == "Graham"
    assert response_data["lastname"] == "Chapman"
    assert "id" in response_data
