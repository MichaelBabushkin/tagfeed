def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    res = res.json()
    assert "message" in res
    assert res.get("message") == "Hello world!"
