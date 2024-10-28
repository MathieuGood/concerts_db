def test_create_show(client):
    response = client.post(
        "/show/",
        json={
            "name": "Rock Am Ring Day 1",
            "event_date": "2022-06-03",
            "comments": "Amazing festival, first time I saw Incubus live!",
            "venue_id": "1",
            "festival_id": "1",
            "attendees_id": "1",
            "concerts": [
                {
                    "artist_id": 1,
                    "comments": "Mike was on fire!",
                    "setlist": "Pardon Me, Stellar, Drive, Wish You Were Here, Megalomaniac, Talk Shows on Mute, Nice to Know You, Warning, Sick Sad Little World, Anna Molly, Love Hurts, Adolescents, Dig, Are You In?, A Crow",
                    "photos": ["Photo of Brandon", "Photo of Mike"],
                    "videos": ["Video of Pardon Me", "Video of Stellar"],
                }
            ],
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Rock Am Ring Day 1"
    assert response_data["event_date"] == "2022-06-03"
    assert (
        response_data["comments"] == "Amazing festival, first time I saw Incubus live!"
    )
    assert response_data["venue_id"] == 1
    assert response_data["festival_id"] == 1
    assert response_data["attendees_id"] == 1
    assert response_data["concerts"][0]["artist_id"] == 1
    assert response_data["concerts"][0]["comments"] == "Mike was on fire!"
    assert (
        response_data["concerts"][0]["setlist"]
        == "Pardon Me, Stellar, Drive, Wish You Were Here, Megalomaniac, Talk Shows on Mute, Nice to Know You, Warning, Sick Sad Little World, Anna Molly, Love Hurts, Adolescents, Dig, Are You In?, A Crow"
    )
    assert response_data["concerts"][0]["photos"] == [
        "Photo of Brandon",
        "Photo of Mike",
    ]
    assert response_data["concerts"][0]["videos"] == [
        "Video of Pardon Me",
        "Video of Stellar",
    ]
    assert "id" in response_data
