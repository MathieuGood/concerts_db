def test_get_all_addresses(client):
    response = client.get(
        "/address/",
    )
    assert response.status_code == 200

    response_data = response.json()
    print("\n----------------- RESPONSE DATA ----------------- ")
    print(response_data)
    assert response_data == []
