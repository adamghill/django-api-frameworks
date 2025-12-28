from datetime import datetime

from django.http import HttpRequest
from ninja import Router, Schema

from car.models import Car

router = Router()


class ListCarResponseItem(Schema):
    id: int
    vin: str
    owner: str
    created_at: datetime
    updated_at: datetime
    car_model_id: int
    car_model_name: str
    car_model_year: int
    color: str


@router.get("/cars/sync-with-schema/", response=dict[str, list[ListCarResponseItem]])
def cars_sync_with_schema(request: HttpRequest):
    return {"results": Car.objects.with_annotations()}


@router.get("/cars/sync-without-schema/", response=dict[str, list[dict]])
def cars_sync_without_schema(request: HttpRequest):
    return {"results": list(Car.objects.as_dicts())}


@router.get("/cars/async-with-schema/", response=dict[str, list[ListCarResponseItem]])
async def cars_async_with_schema(request: HttpRequest):
    return {"results": [car async for car in Car.objects.with_annotations().aiterator()]}


@router.get("/cars/async-without-schema/", response=dict[str, list[dict]])
async def cars_async_without_schema(request: HttpRequest):
    return {"results": [car async for car in Car.objects.as_dicts().aiterator()]}


@router.get("/cars/", response=dict[str, list[dict]])
async def cars(request: HttpRequest):
    return await cars_async_without_schema(request)
