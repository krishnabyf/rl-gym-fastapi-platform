def test_benchmark_compares_policies(client):
    response = client.post(
        "/api/v1/benchmarks",
        json={
            "environment_id": "gridworld-v0",
            "policies": ["random", "greedy"],
            "episodes": 4,
            "max_steps": 50,
            "seed": 7,
        },
    )

    assert response.status_code == 202
    job_id = response.json()["id"]

    result = client.get(f"/api/v1/benchmarks/{job_id}")

    assert result.status_code == 200
    payload = result.json()
    assert payload["best_policy"] == "greedy"
    assert len(payload["policies"]) == 2


def test_benchmark_rejects_duplicate_policies(client):
    response = client.post(
        "/api/v1/benchmarks",
        json={"policies": ["greedy", "greedy"], "episodes": 2},
    )

    assert response.status_code == 422

