def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to the 'Concerts I Have Been To' API"
