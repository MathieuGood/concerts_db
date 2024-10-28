def test_venue_create(client):
    response = client.post(
        "/venue/",
        json={
            "name": "Nürburgring",
            "address_id": "1",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Nürburgring"
    assert response_data["address_id"] == 1
    assert "id" in response_data
