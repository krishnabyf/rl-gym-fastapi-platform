def test_list_environments(client):
    response = client.get("/api/v1/environments")

    assert response.status_code == 200
    environments = response.json()
    assert environments[0]["id"] == "gridworld-v0"
    assert "right" in environments[0]["action_space"]


def test_get_unknown_environment_returns_404(client):
    response = client.get("/api/v1/environments/unknown-v0")

    assert response.status_code == 404

