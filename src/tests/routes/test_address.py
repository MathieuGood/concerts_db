def test_create_address(client):
    response = client.post(
        "/address/",
        json={
            "city": "Springfield",
            "country": "USA",
        },
    )
    # assert response.status_code == 200
    response_data = response.json()
    # assert response_data == "Springfield"
    assert response_data["city"] == "Springfield"
    assert response_data["country"] == "USA"
    assert "id" in response_data
