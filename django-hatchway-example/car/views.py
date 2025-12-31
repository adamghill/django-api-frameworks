from hatchway import api_view

from car.models import Car
from car.schemas import CarsListResponseSchema


@api_view.get(validate_output=False)
def cars_hatchway_sync(request) -> CarsListResponseSchema:
    """
    Returns a list of cars using Hatchway with synchronous ORM queries.
    Uses Hatchway's built-in msgspec serialization and schema validation.
    """
    cars = Car.objects.as_dicts()
    return {"results": list(cars)}


@api_view.get(validate_output=False)
async def cars_hatchway_async(request) -> CarsListResponseSchema:
    """
    Returns a list of cars using Hatchway with asynchronous ORM queries.
    Uses Hatchway's built-in msgspec serialization and schema validation.
    """
    cars = Car.objects.as_dicts()

    cars_list = []
    async for car in cars.aiterator():
        cars_list.append(car)

    return {"results": cars_list}
