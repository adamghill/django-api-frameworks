from datetime import datetime

from hatchway import Schema


class CarResponseSchema(Schema):
    """Schema for car response with flattened model information"""

    id: int
    vin: str
    owner: str
    created_at: datetime
    updated_at: datetime
    car_model_id: int
    car_model_name: str
    car_model_year: int
    color: str


class CarsListResponseSchema(Schema):
    """Schema for list of cars response"""

    results: list[CarResponseSchema]
