import json
from typing import Any

import pytest
import requests

"""
Ports to project mapping:

8001 - django
8002 - django-ninja
8003 - django-shinobi
8004 - django-rapid
8005 - django-bolt
8006 - djangorestframework
8007 - djrest2
8099 - fastapi
"""

# API configurations for different implementations
API_CONFIGS = {
    "django": {
        "base_url": "http://localhost:8001",
        "endpoints": [
            "/api/cars-orjson-sync/",
            "/api/cars-orjson-async/",
            "/api/cars-streaming/",
            "/api/cars-asyncpg/",
            "/api/cars-msgspec/",
            "/api/cars-json/",
            "/api/cars-raw-sync/",
            "/api/cars-postgres-json/",
            "/api/cars-pydantic/",
        ],
    },
    "django-hatchway": {
        "base_url": "http://localhost:7999",
        "endpoints": [
            "/api/cars/",
        ],
    },
    "django-ninja": {
        "base_url": "http://localhost:8002",
        "endpoints": [
            "/api/cars/sync-with-schema/",
            "/api/cars/sync-without-schema/",
            "/api/cars/async-with-schema/",
            "/api/cars/async-without-schema/",
        ],
    },
    "django-shinobi": {
        "base_url": "http://localhost:8003",
        "endpoints": [
            "/api/cars/sync-with-schema/",
            "/api/cars/sync-without-schema/",
            "/api/cars/async-with-schema/",
            "/api/cars/async-without-schema/",
        ],
    },
    "django-rapid": {
        "base_url": "http://localhost:8004",
        "endpoints": [
            "/api/cars/",
        ],
    },
    "django-bolt": {
        "base_url": "http://localhost:8005",
        "endpoints": [
            "/api/cars-serialized/",
            "/api/cars-dicts/",
        ],
    },
    "djangorestframework": {
        "base_url": "http://localhost:8006",
        "endpoints": [
            "/api/cars-serialized/",
            "/api/cars-orjson/",
            "/api/cars-dict-orjson/",
        ],
    },
    "djrest2": {
        "base_url": "http://localhost:8007",
        "endpoints": [
            "/api/cars-json/",
            "/api/cars-queryset-as-dicts/",
        ],
    },
    "fastapi": {
        "base_url": "http://localhost:8099",
        "endpoints": [
            "/api/cars/",
        ],
    },
}

FIELDS = [
    "id",
    "vin",
    "owner",
    "created_at",
    "updated_at",
    "car_model_id",
    "car_model_name",
    "car_model_year",
    "color",
]


def fetch_api_data(service: str, endpoint: str) -> list[dict[str, Any]]:
    """
    Fetch data from a specific API endpoint.
    """
    config = API_CONFIGS[service]
    url = f"{config['base_url']}{endpoint}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        assert "results" in data, f"Expected 'results' key in response from {url}"

        return data["results"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to fetch data from {url}: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON response from {url}: {e}")
