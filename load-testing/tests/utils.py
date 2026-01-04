import json
from typing import Any

import pytest
import requests

"""
Ports to project mapping:

8001 - django-wsgi
8002 - django-asgi
8003 - django-rsgi
8004 - django-ninja
8005 - django-shinobi
8006 - django-rapid
8007 - django-bolt
8008 - djangorestframework
8009 - djrest2
8099 - fastapi
"""

# API configurations for different implementations
API_CONFIGS = {
    "django-wsgi": {
        "base_url": "http://localhost:8001",
        "endpoints": {
            "orm": [
                "/api/cars-orjson-sync/",
                "/api/cars-msgspec/",
                "/api/cars-json/",
                "/api/cars-raw-sync/",
                "/api/cars-postgres-json/",
                "/api/cars-pydantic/",
                "/api/cars-generated-field/",
                "/api/cars-generated-field-concat/",
            ],
            "json": [
                "/api/json-sync/",
                "/api/json-orjson-sync/",
                "/api/json-msgspec-sync/",
                "/api/json-async/",
                "/api/json-orjson-async/",
                "/api/json-msgspec-async/",
            ],
        },
    },
    "django-asgi": {
        "base_url": "http://localhost:8002",
        "endpoints": {
            "orm": [
                "/api/cars-orjson-sync/",
                "/api/cars-orjson-async/",
                "/api/cars-streaming/",
                "/api/cars-asyncpg/",
                "/api/cars-msgspec/",
                "/api/cars-json/",
                "/api/cars-raw-sync/",
                "/api/cars-postgres-json/",
                "/api/cars-pydantic/",
                "/api/cars-generated-field/",
                "/api/cars-generated-field-concat/",
            ],
            "json": [
                "/api/json-sync/",
                "/api/json-orjson-sync/",
                "/api/json-msgspec-sync/",
                "/api/json-async/",
                "/api/json-orjson-async/",
                "/api/json-msgspec-async/",
            ],
        },
    },
    "django-rsgi": {
        "base_url": "http://localhost:8003",
        "endpoints": {
            "orm": [],
            "json": [
                "/api/json-sync/",
                "/api/json-orjson-sync/",
                "/api/json-msgspec-sync/",
                "/api/json-async/",
                "/api/json-orjson-async/",
                "/api/json-msgspec-async/",
            ],
        },
    },
    "django-uvicorn": {
        "base_url": "http://localhost:8004",
        "endpoints": {
            "orm": [],
            "json": [
                "/api/json-sync/",
                "/api/json-orjson-sync/",
                "/api/json-msgspec-sync/",
                "/api/json-async/",
                "/api/json-orjson-async/",
                "/api/json-msgspec-async/",
            ],
        },
    },
    "django-ninja": {
        "base_url": "http://localhost:8010",
        "endpoints": {
            "orm": [
                "/api/cars/sync-with-schema/",
                "/api/cars/sync-without-schema/",
                "/api/cars/async-with-schema/",
                "/api/cars/async-without-schema/",
            ],
            "json": [],
        },
    },
    "django-shinobi": {
        "base_url": "http://localhost:8011",
        "endpoints": {
            "orm": [
                "/api/cars/sync-with-schema/",
                "/api/cars/sync-without-schema/",
                "/api/cars/async-with-schema/",
                "/api/cars/async-without-schema/",
            ],
            "json": [],
        },
    },
    "django-rapid": {
        "base_url": "http://localhost:8012",
        "endpoints": {
            "orm": [
                "/api/cars/",
            ],
            "json": [],
        },
    },
    "django-bolt": {
        "base_url": "http://localhost:8013",
        "endpoints": {
            "orm": [
                "/api/cars-serialized/",
                "/api/cars-dicts/",
            ],
            "json": [],
        },
    },
    "djangorestframework": {
        "base_url": "http://localhost:8014",
        "endpoints": {
            "orm": [
                "/api/cars-serialized/",
                "/api/cars-orjson/",
                "/api/cars-dict-orjson/",
            ],
            "json": [],
        },
    },
    "djrest2": {
        "base_url": "http://localhost:8015",
        "endpoints": {
            "orm": [
                "/api/cars-json/",
                "/api/cars-queryset-as-dicts/",
            ],
            "json": [],
        },
    },
    "fastapi": {
        "base_url": "http://localhost:8030",
        "endpoints": {
            "orm": [
                "/api/cars/",
            ],
            "json": [
                "/api/json/",
            ],
        },
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
