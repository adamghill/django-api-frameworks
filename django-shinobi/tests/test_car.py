import pytest
from car.models import Car, CarModel


@pytest.fixture
def create_test_data(db):
    model = CarModel.objects.create(
        name="Test Model",
        make="Test Make",
        year=2024,
        color="Red",
        price=50000.00,
    )
    Car.objects.create(vin="VIN-123", model=model, owner="Test Owner")


@pytest.mark.django_db
def test_list_cars(client, create_test_data):
    response = client.get("/api/cars/")

    assert 200 == response.status_code

    actual = response.json()
    results = actual["results"]
    assert 1 == len(results)
    assert "VIN-123" == results[0]["vin"]
    assert "Test Model" == results[0]["car_model_name"]
