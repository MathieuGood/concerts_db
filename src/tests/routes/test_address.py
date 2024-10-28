def test_address_create(client):
    response = client.post(
        "/address/",
        json={
            "city": "Springfield",
            "country": "USA",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["city"] == "Springfield"
    assert response_data["country"] == "USA"
    assert "id" in response_data


def test_address_get_all(client):
    response = client.get(
        "/address/",
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= 0
    assert response_data[0]["city"] == "Los Angeles"
    assert response_data[0]["country"] == "USA"


def test_address_get(client):
    response = client.get(
        "/address/1",
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["city"] == "Los Angeles"
    assert response_data["country"] == "USA"
