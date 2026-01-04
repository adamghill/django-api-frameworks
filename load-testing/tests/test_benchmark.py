import subprocess

import pytest
from tests.utils import API_CONFIGS, fetch_api_data


@pytest.mark.parametrize(
    "service,category,endpoint",
    [
        (service, category, endpoint)
        for service, config in API_CONFIGS.items()
        for category, endpoints in config["endpoints"].items()
        for endpoint in endpoints
    ],
)
def test_endpoints(benchmark, service, category, endpoint):
    """
    Compare performance across active endpoints.
    Tests are grouped by category (orm or json) for accurate comparison.
    """
    benchmark.group = f"api_comparison_{category}"

    def make_request():
        return fetch_api_data(service, endpoint)

    # Benchmark this specific endpoint with pedantic mode for more accurate results
    result = benchmark.pedantic(make_request, rounds=10, warmup_rounds=3)

    # Verify the response is valid
    assert isinstance(result, dict) or isinstance(result, list), f"Invalid response format from {service} {endpoint}"


@pytest.mark.parametrize(
    "service,category,endpoint",
    [
        (service, category, endpoint)
        for service, config in API_CONFIGS.items()
        for category, endpoints in config["endpoints"].items()
        for endpoint in endpoints
    ],
)
def test_wrk_endpoints(service, category, endpoint):
    """
    Measure performance across active endpoints using wrk.
    """
    config = API_CONFIGS[service]
    url = f"{config['base_url']}{endpoint}"

    # Run wrk for 5 seconds with 10 connections and 2 threads
    cmd = ["wrk", "-t2", "-c10", "-d5s", url]

    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Output the results so they can be seen in the test logs
        print(f"\nResults for {service} ({category}) {endpoint}:\n{process.stdout}")

        # Basic validation that wrk ran successfully and got some results
        assert "Requests/sec:" in process.stdout
        assert "Transfer/sec:" in process.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"wrk failed for {url} with exit code {e.returncode}: {e.stderr}")
