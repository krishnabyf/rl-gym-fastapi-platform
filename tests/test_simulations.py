def test_create_and_fetch_simulation(client):
    response = client.post(
        "/api/v1/simulations",
        json={
            "environment_id": "gridworld-v0",
            "episodes": 3,
            "max_steps": 20,
            "policy": "greedy",
            "seed": 42,
        },
    )

    assert response.status_code == 202
    job_id = response.json()["id"]

    result = client.get(f"/api/v1/simulations/{job_id}")

    assert result.status_code == 200
    payload = result.json()
    assert payload["success_rate"] == 1.0
    assert payload["average_reward"] > 0
    assert len(payload["metrics"]) == 3


def test_invalid_policy_is_rejected(client):
    response = client.post(
        "/api/v1/simulations",
        json={"environment_id": "gridworld-v0", "episodes": 1, "policy": "not-real"},
    )

    assert response.status_code == 422

