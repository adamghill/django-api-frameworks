import json
from functools import lru_cache

import msgspec
import orjson
import pydantic
from django.contrib.postgres.aggregates import JSONBAgg
from django.db import connection
from django.db.models import CharField, F, Func, JSONField, TextField
from django.db.models.functions import Cast, JSONObject
from django.http import HttpResponse, StreamingHttpResponse

from car.asyncpg_manager import AsyncpgManager
from car.models import Car


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


def json_sync(request):
    return HttpResponse(content=json.dumps(get_complex_json()), content_type="application/json")


def json_orjson_sync(request):
    return HttpResponse(content=orjson.dumps(get_complex_json()), content_type="application/json")


def json_msgspec_sync(request):
    return HttpResponse(content=msgspec.json.encode(get_complex_json()), content_type="application/json")


async def json_async(request):
    return HttpResponse(content=json.dumps(get_complex_json()), content_type="application/json")


async def json_orjson_async(request):
    return HttpResponse(content=orjson.dumps(get_complex_json()), content_type="application/json")


async def json_msgspec_async(request):
    return HttpResponse(content=msgspec.json.encode(get_complex_json()), content_type="application/json")


class CarResponse(pydantic.BaseModel):
    id: int
    vin: str
    owner: str
    created_at: str
    updated_at: str
    car_model_id: int
    car_model_name: str
    car_model_year: int
    color: str

    class Config:
        from_attributes = True


class CarsListResponse(pydantic.BaseModel):
    results: list[CarResponse]


def json_default(obj):
    if hasattr(obj, "isoformat"):
        return obj.isoformat()[:-6] + "Z"

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def cars_json(request):
    """
    Returns a list of cars with their model information.
    """

    cars = Car.objects.as_dicts()

    return HttpResponse(
        json.dumps({"results": list(cars)}, default=json_default),
        content_type="application/json",
    )


def cars_msgspec(request):
    """
    Returns a list of cars with their model information.
    """

    cars = Car.objects.as_dicts()

    return HttpResponse(
        msgspec.json.encode(
            {"results": list(cars)},
        ),
        content_type="application/json",
    )


def cars_pydantic(request):
    """
    Returns a list of cars with their model information using Pydantic serialization.
    """

    cars = Car.objects.as_dicts()

    # Convert datetime objects to ISO format strings for Pydantic
    formatted_cars = []
    for car in cars:
        formatted_car = {
            **car,
            "created_at": car["created_at"].isoformat()[:-6] + "Z" if car["created_at"] else None,
            "updated_at": car["updated_at"].isoformat()[:-6] + "Z" if car["updated_at"] else None,
        }
        formatted_cars.append(CarResponse(**formatted_car))

    response_data = CarsListResponse(results=formatted_cars)

    return HttpResponse(
        response_data.model_dump_json(),
        content_type="application/json",
    )


def cars_orjson_sync(request):
    """
    Returns a list of cars with their model information.
    """

    cars = Car.objects.as_dicts()

    return HttpResponse(
        orjson.dumps(
            {"results": list(cars)},
            option=orjson.OPT_PASSTHROUGH_DATETIME,
            default=json_default,
        ),
        content_type="application/json",
    )


async def cars_orjson_async(request):
    """
    Returns a list of cars with their model information.
    Optimized version using custom queryset method and aiterator().
    """

    cars = Car.objects.as_dicts()

    cars_list = []
    async for car in cars.aiterator():
        cars_list.append(car)

    return HttpResponse(
        orjson.dumps(
            {"results": cars_list},
            option=orjson.OPT_PASSTHROUGH_DATETIME,
            default=json_default,
        ),
        content_type="application/json",
    )


async def cars_streaming(request):
    """
    Returns a list of cars with their model information.
    """

    cars_queryset = (
        Car.objects.select_related("model")
        .annotate(
            car_model_id=F("model_id"),
            car_model_name=F("model__name"),
            car_model_year=F("model__year"),
            color=F("model__color"),
        )
        .values(
            "id",
            "vin",
            "owner",
            "created_at",
            "updated_at",
            "car_model_id",
            "car_model_name",
            "car_model_year",
            "color",
        )
    )

    async def generate():
        yield '{"results": ['
        first = True

        async for car in cars_queryset.aiterator(chunk_size=1000):  # Process in chunks
            if not first:
                yield ","

            first = False

            yield orjson.dumps(car, option=orjson.OPT_PASSTHROUGH_DATETIME, default=json_default)

        yield "]}"

    response = StreamingHttpResponse(generate(), content_type="application/json")
    response["Cache-Control"] = "no-cache"

    return response


async def cars_asyncpg(request):
    """
    Use asyncpg directly.
    """

    cars_list = await AsyncpgManager().get_cars()

    return HttpResponse(
        orjson.dumps(
            {"results": cars_list},
            option=orjson.OPT_PASSTHROUGH_DATETIME,
            default=json_default,
        ),
        content_type="application/json",
    )


def cars_raw_sync(request):
    """
    Use raw SQL through Django cursor, bypassing model layer.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                c.id,
                c.vin,
                c.owner,
                c.created_at,
                c.updated_at,
                c.model_id as car_model_id,
                cm.name as car_model_name,
                cm.year as car_model_year,
                cm.color
            FROM car_car c
            JOIN car_carmodel cm ON c.model_id = cm.id
            """
        )
        columns = [col[0] for col in cursor.description]
        cars = [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]

    return HttpResponse(
        orjson.dumps(
            {"results": cars},
            option=orjson.OPT_PASSTHROUGH_DATETIME,
            default=json_default,
        ),
        content_type="application/json",
    )


def cars_postgres_json(request):
    """
    Offload JSON generation to Postgres.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT json_build_object('results', json_agg(t))::text
            FROM (
                SELECT
                    c.id,
                    c.vin,
                    c.owner,
                    to_char(c.created_at AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') as created_at,
                    to_char(c.updated_at AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') as updated_at,
                    c.model_id as car_model_id,
                    cm.name as car_model_name,
                    cm.year as car_model_year,
                    cm.color
                FROM car_car c
                JOIN car_carmodel cm ON c.model_id = cm.id
            ) t
            """
        )
        result = cursor.fetchone()[0]

    return HttpResponse(
        result,
        content_type="application/json",
    )


def cars_postgres_json_orm(request):
    """
    Offload JSON generation to Postgres using Django ORM.
    """

    class ToChar(Func):
        function = "to_char"
        template = "%(function)s(%(expressions)s AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS.US\"Z\"')"
        output_field = CharField()

    formatted_created_at = ToChar(F("created_at"))
    formatted_updated_at = ToChar(F("updated_at"))

    data = Car.objects.select_related("model").aggregate(
        result=Cast(
            JSONObject(
                results=JSONBAgg(
                    JSONObject(
                        id=F("id"),
                        vin=F("vin"),
                        owner=F("owner"),
                        created_at=formatted_created_at,
                        updated_at=formatted_updated_at,
                        car_model_id=F("model_id"),
                        car_model_name=F("model__name"),
                        car_model_year=F("model__year"),
                        color=F("model__color"),
                    )
                )
            ),
            output_field=TextField(),
        )
    )

    return HttpResponse(
        data["result"],
        content_type="application/json",
    )


def cars_generated_field(request):
    """
    Returns a list of cars using the GeneratedField on the model.
    Note: GeneratedField cannot include joined fields or auto-updated timestamps,
    so we merge those in the query.
    """

    class ToChar(Func):
        function = "to_char"
        template = "%(function)s(%(expressions)s AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS.US\"Z\"')"
        output_field = CharField()

    formatted_created_at = ToChar(F("created_at"))
    formatted_updated_at = ToChar(F("updated_at"))

    data = Car.objects.select_related("model").aggregate(
        results=JSONBAgg(
            JSONObject(
                # Spread the json_data GeneratedField
                id=F("json_data__id"),
                vin=F("json_data__vin"),
                owner=F("json_data__owner"),
                created_at=formatted_created_at,
                updated_at=formatted_updated_at,
                car_model_id=F("json_data__car_model_id"),
                # Add the joined model fields
                car_model_name=F("model__name"),
                car_model_year=F("model__year"),
                color=F("model__color"),
            )
        )
    )

    return HttpResponse(content=msgspec.json.encode(data), content_type="application/json")


def cars_generated_field_concat(request):
    """
    Returns a list of cars using GeneratedFields from both Car and CarModel.
    Uses Postgres || operator to merge the two JSON objects.
    """

    class ToChar(Func):
        function = "to_char"
        template = "%(function)s(%(expressions)s AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS.US\"Z\"')"
        output_field = CharField()

    class JSONConcat(Func):
        """Postgres || operator for JSONB concatenation"""

        function = ""
        template = "(%(expressions)s)"
        arg_joiner = " || "
        output_field = JSONField()

    formatted_created_at = ToChar(F("created_at"))
    formatted_updated_at = ToChar(F("updated_at"))

    results = Car.objects.select_related("model").aggregate(
        results=JSONBAgg(
            JSONConcat(
                F("json_data"),
                F("model__json_data"),
                JSONObject(
                    created_at=formatted_created_at,
                    updated_at=formatted_updated_at,
                ),
            ),
        )
    )

    return HttpResponse(content=msgspec.json.encode(results), content_type="application/json")
