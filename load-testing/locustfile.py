import threading

from locust import FastHttpUser, between, tag, task
from tests.utils import API_CONFIGS

# Create a global lock object
task_lock = threading.Lock()


class ApiLoadTest(FastHttpUser):
    wait_time = between(1, 3)  # Time between tasks (1 to 3 seconds)
    host = "http://localhost"


def create_task(service, category, endpoint):
    """
    Dynamically create a task function for the given service, category, and endpoint.
    """

    @tag(service, category)
    @task(1)
    def task_func(self):
        # In Docker context, use service name as hostname and port 8000
        url = f"http://{service}:8000{endpoint}"
        with task_lock:
            self.client.get(url, name=f"{service} [{category}] {endpoint}")

    return task_func


# Dynamically add tasks to ApiLoadTest based on API_CONFIGS
for service, config in API_CONFIGS.items():
    for category, endpoints in config["endpoints"].items():
        for endpoint in endpoints:
            # Create a unique task name
            safe_endpoint = endpoint.strip("/").replace("/", "_").replace("-", "_")
            task_name = f"test_{service.replace('-', '_')}_{category}_{safe_endpoint}"

            # Add the task to the class
            setattr(ApiLoadTest, task_name, create_task(service, category, endpoint))
