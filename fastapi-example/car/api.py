from datetime import datetime
from functools import lru_cache
from typing import Annotated

from database import get_db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from car.service import CarService

router = APIRouter()


class CarSchema(BaseModel):
    id: int
    vin: str
    owner: str
    created_at: datetime
    updated_at: datetime
    car_model_id: int
    car_model_name: str
    car_model_year: int
    color: str


@router.get("/cars/", response_model=dict[str, list[CarSchema]])
async def list_cars(db: Annotated[AsyncSession, Depends(get_db)]):
    cars = await CarService(db).retrieve_all_cars()

    return {"results": cars}


@lru_cache
def get_complex_json():
    results = []

    for idx in range(1, 10000):
        results.append(
            {
                "id": idx,
                "vin": "1234567890",
                "owner": "John Doe",
                "created_at": "2022-01-01T00:00:00Z",
                "updated_at": "2022-01-01T00:00:00Z",
                "car_model_id": 1,
                "car_model_name": "Model S",
                "car_model_year": 2022,
                "color": "Red",
            }
        )

    return {"results": results}


@router.get("/json/", response_model=dict)
async def json_endpoint():
    return get_complex_json()
