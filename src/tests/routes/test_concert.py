def test_create_concert(client):
    response = client.post(
        "/concert/",
        json={
            "comments": "Best concert ever!",
            "setlist": "Pardon Me, Stellar, Drive, Wish You Were Here, Megalomaniac, Talk Shows on Mute, Nice to Know You, Warning, Sick Sad Little World, Anna Molly, Love Hurts, Adolescents, Dig, Are You In?, A Crow",
            "show_id": "1",
            "artist_id": "1",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["comments"] == "Best concert ever!"
    assert (
        response_data["setlist"]
        == "Pardon Me, Stellar, Drive, Wish You Were Here, Megalomaniac, Talk Shows on Mute, Nice to Know You, Warning, Sick Sad Little World, Anna Molly, Love Hurts, Adolescents, Dig, Are You In?, A Crow"
    )
    assert response_data["show_id"] == 1
    assert response_data["artist_id"] == 1
    assert "id" in response_data
