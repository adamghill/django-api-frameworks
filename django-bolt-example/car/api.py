from datetime import datetime
from typing import Any

from django_bolt import BoltAPI
from django_bolt.serializers import Serializer
import msgspec
from car.models import Car

api = BoltAPI()


class CarSerializer(msgspec.Struct):
    id: int
    vin: str
    owner: str
    created_at: datetime
    updated_at: datetime
    car_model_id: int
    car_model_name: str
    car_model_year: int
    color: str



@api.get("/cars")
async def cars():
    return await cars_serialized()


@api.get("/cars-serialized")
async def cars_serialized():
    cars = []

    async for car in Car.objects.with_annotations():
        cars.append(CarSerializer(
            id=car.id,
            vin=car.vin,
            owner=car.owner,
            created_at=car.created_at,
            updated_at=car.updated_at,
            car_model_id=car.car_model_id,
            car_model_name=car.car_model_name,
            car_model_year=car.car_model_year,
            color=car.color,
        ))

    return {"results": cars}


@api.get("/cars-dicts")
async def cars_as_dicts():
    cars = []

    async for car_dict in Car.objects.as_dicts():
        cars.append(car_dict)

    return {"results": cars}
