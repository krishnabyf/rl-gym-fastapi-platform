# Production Notes

## Deployment

Run the API behind a reverse proxy or managed container platform. For larger workloads, move background execution to a queue such as Celery, Dramatiq, Arq, or a cloud-native worker service.

## Persistence

The demo uses an in-memory job store to keep the repository simple. In production, replace `JobStore` with a repository backed by PostgreSQL. Suggested tables:

- `jobs`: id, kind, status, payload, result, error, created_at, updated_at
- `episode_metrics`: job_id, episode, steps, reward, success, final_observation
- `benchmark_results`: job_id, policy, average_reward, success_rate, average_steps

## Observability

Add structured JSON logs, request IDs, latency histograms, and job duration metrics. Recommended metrics:

- API request count and latency by route/status.
- Simulation job duration and failure rate.
- Episode reward distribution.
- Benchmark success rate by policy and environment.

## Security

For client-facing deployment, add authentication, per-user job ownership, rate limiting, request-size limits, and audit logs. Keep user-submitted environment code isolated in a worker sandbox.

## Scaling

The API layer should stay stateless. Run multiple API replicas and scale worker replicas independently based on queue depth and CPU utilization.

