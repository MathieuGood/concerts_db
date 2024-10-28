def test_create_video(client):
    response = client.post(
        "/video/",
        json={
            "path": "https://picsum.photos/200/300",
               "concert_id": "1",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["path"] == "https://picsum.photos/200/300"
    assert response_data["concert_id"] == 1
    assert "id" in response_data
