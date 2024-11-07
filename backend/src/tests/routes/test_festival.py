def test_festival_create(client):
    response = client.post(
        "/festival/",
        json={
            "name": "Rock Am Ring",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Rock Am Ring"
    assert "id" in response_data
