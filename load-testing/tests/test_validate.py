import pytest
import requests
from tests.utils import API_CONFIGS, FIELDS, fetch_api_data


def test_all_apis_return_data():
    """
    Test that all API endpoints return data successfully.
    """
    failed_endpoints = []

    for service, config in API_CONFIGS.items():
        for category, endpoints in config["endpoints"].items():
            for endpoint in endpoints:
                url = f"{config['base_url']}{endpoint}"

                try:
                    response = requests.get(url, timeout=None)

                    if response.status_code != 200:
                        failed_endpoints.append(f"{url}: {response.status_code}")
                except requests.exceptions.RequestException:
                    failed_endpoints.append(f"{url}: Connection failed")

    if failed_endpoints:
        pytest.fail(f"Failed endpoints: {failed_endpoints}")


def test_api_data_consistency():
    """
    Test that all APIs return consistent car data.
    This is the main test that verifies data consistency across implementations.
    """

    # Collect data from all endpoints
    all_api_data = {}

    for service, config in API_CONFIGS.items():
        service_data = {}

        for category, endpoints in config["endpoints"].items():
            for endpoint in endpoints:
                try:
                    data = fetch_api_data(service, endpoint)

                    service_data[endpoint] = data
                except Exception:
                    # Skip endpoints that fail and continue with others
                    continue

        all_api_data[service] = service_data

    if not all_api_data:
        pytest.fail("No API endpoints returned data successfully")

    # Get the first successful API response as reference
    reference_data = None

    for service, endpoints in all_api_data.items():
        for endpoint, data in endpoints.items():
            if data:  # Found non-empty data
                reference_data = data
                break
        if reference_data:
            break

    if not reference_data:
        pytest.fail("No API endpoints returned non-empty data")

    # Compare all other API responses with the reference
    inconsistencies = []

    for service, endpoints in all_api_data.items():
        for endpoint, data in endpoints.items():
            if not data:
                continue

            current_endpoint = f"{service}{endpoint}"

            # Check if data length matches
            if len(data) != len(reference_data):
                inconsistencies.append(
                    f"{current_endpoint}: Length mismatch (expected {len(reference_data)}, got {len(data)})"
                )
                continue

            # Check each car record
            for i, (ref_car, current_car) in enumerate(zip(reference_data, data)):
                # Compare key fields
                for field in FIELDS:
                    ref_value = ref_car.get(field)
                    current_value = current_car.get(field)

                    if ref_value != current_value:
                        inconsistencies.append(
                            f"{current_endpoint}: Car {i} {field} mismatch (expected {ref_value}, got {current_value})"
                        )

    if inconsistencies:
        pytest.fail("Data inconsistencies found:\n" + "\n".join(inconsistencies))


def test_api_response_structure():
    """
    Test that all APIs return data with the expected structure.
    """

    structure_issues = []

    for service, config in API_CONFIGS.items():
        for category, endpoints in config["endpoints"].items():
            for endpoint in endpoints:
                try:
                    data = fetch_api_data(service, endpoint)

                    if not data:
                        structure_issues.append(f"{service}{endpoint}: Empty response")
                        continue

                    # Check first car record structure
                    car = data[0]

                    # Check required fields
                    missing_required = [field for field in FIELDS if field not in car]

                    if missing_required:
                        structure_issues.append(f"{service}{endpoint}: Missing required fields: {missing_required}")
                except Exception as e:
                    structure_issues.append(f"{service}{endpoint}: Error - {str(e)}")

    if structure_issues:
        pytest.fail("Structure issues found:\n" + "\n".join(structure_issues))
