from datetime import datetime
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
