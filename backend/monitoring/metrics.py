from prometheus_client import Counter

telemetry_requests_total = Counter(
    'telemetry_requests_total',
    'Total telemetry requests received'
)

telemetry_failures_total = Counter(
    'telemetry_failures_total',
    'Total failed telemetry requests'
)