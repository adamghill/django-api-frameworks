import threading

from locust import FastHttpUser, between, tag, task

# Create a global lock object
task_lock = threading.Lock()


class ApiLoadTest(FastHttpUser):
    wait_time = between(1, 3)  # Time between tasks (1 to 3 seconds)
    host = "http://localhost"

    # django
    @tag("django")
    @task(1)
    def test_django_api_cars_orjson_sync(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-orjson-sync/")

    @tag("django")
    @task(1)
    def test_django_api_cars_orjson_async(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-orjson-async/")

    @tag("django")
    @task(1)
    def test_django_api_cars_streaming(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-streaming/")

    @tag("django")
    @task(1)
    def test_django_api_cars_asyncpg(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-asyncpg/")

    @tag("django")
    @task(1)
    def test_django_api_cars_msgspec(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-msgspec/")

    @tag("django")
    @task(1)
    def test_django_api_cars_json(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-json/")

    @tag("django")
    @task(1)
    def test_django_api_cars_raw_sync(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-raw-sync/")

    @tag("django")
    @task(1)
    def test_django_api_cars_postgres_json(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-postgres-json/")

    @tag("django")
    @task(1)
    def test_django_api_cars_pydantic(self):
        with task_lock:
            self.client.get("http://django:8000/api/cars-pydantic/")

    # django-ninja
    @tag("django-ninja")
    @task(1)
    def test_django_ninja_api_cars_sync_with_schema(self):
        with task_lock:
            self.client.get("http://django-ninja:8000/api/cars/sync-with-schema/")

    @tag("django-ninja")
    @task(1)
    def test_django_ninja_api_cars_sync_without_schema(self):
        with task_lock:
            self.client.get("http://django-ninja:8000/api/cars/sync-without-schema/")

    @tag("django-ninja")
    @task(1)
    def test_django_ninja_api_cars_async_with_schema(self):
        with task_lock:
            self.client.get("http://django-ninja:8000/api/cars/async-with-schema/")

    @tag("django-ninja")
    @task(1)
    def test_django_ninja_api_cars_async_without_schema(self):
        with task_lock:
            self.client.get("http://django-ninja:8000/api/cars/async-without-schema/")

    # django-shinobi
    @tag("django-shinobi")
    @task(1)
    def test_django_shinobi_api_cars_sync_with_schema(self):
        with task_lock:
            self.client.get("http://django-shinobi:8000/api/cars/sync-with-schema/")

    @tag("django-shinobi")
    @task(1)
    def test_django_shinobi_api_cars_sync_without_schema(self):
        with task_lock:
            self.client.get("http://django-shinobi:8000/api/cars/sync-without-schema/")

    @tag("django-shinobi")
    @task(1)
    def test_django_shinobi_api_cars_async_with_schema(self):
        with task_lock:
            self.client.get("http://django-shinobi:8000/api/cars/async-with-schema/")

    @tag("django-shinobi")
    @task(1)
    def test_django_shinobi_api_cars_async_without_schema(self):
        with task_lock:
            self.client.get("http://django-shinobi:8000/api/cars/async-without-schema/")

    # django-rapid
    @tag("django-rapid")
    @task(1)
    def test_django_rapid_api_cars(self):
        with task_lock:
            self.client.get("http://django-rapid:8000/api/cars/")

    # django-bolt
    @tag("django-bolt")
    @task(1)
    def test_django_bolt_api_cars_serialized(self):
        with task_lock:
            self.client.get("http://django-bolt:8000/api/cars-serialized/")

    @tag("django-bolt")
    @task(1)
    def test_django_bolt_api_cars_dicts(self):
        with task_lock:
            self.client.get("http://django-bolt:8000/api/cars-dicts/")

    # djangorestframework
    @tag("djangorestframework")
    @task(1)
    def test_djangorestframework_api_cars_serialized(self):
        with task_lock:
            self.client.get("http://djangorestframework:8000/api/cars-serialized/")

    @tag("djangorestframework")
    @task(1)
    def test_djangorestframework_api_cars_orjson(self):
        with task_lock:
            self.client.get("http://djangorestframework:8000/api/cars-orjson/")

    @tag("djangorestframework")
    @task(1)
    def test_djangorestframework_api_cars_dict_orjson(self):
        with task_lock:
            self.client.get("http://djangorestframework:8000/api/cars-dict-orjson/")

    # djrest2
    @tag("djrest2")
    @task(1)
    def test_djrest2_api_cars_json(self):
        with task_lock:
            self.client.get("http://djrest2:8000/api/cars-json/")

    @tag("djrest2")
    @task(1)
    def test_djrest2_api_cars_orjson(self):
        with task_lock:
            self.client.get("http://djrest2:8000/api/cars-orjson/")

    # fastapi
    @tag("fastapi")
    @task(1)
    def test_fastapi_api_cars(self):
        with task_lock:
            self.client.get("http://fastapi:8000/api/cars/")
