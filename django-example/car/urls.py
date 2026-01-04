from django.urls import path

from car import views

urlpatterns = [
    path("cars-orjson-sync/", views.cars_orjson_sync),
    path("cars-orjson-async/", views.cars_orjson_async),
    path("cars-streaming/", views.cars_streaming),
    path("cars-asyncpg/", views.cars_asyncpg),
    path("cars-msgspec/", views.cars_msgspec),
    path("cars-json/", views.cars_json),
    path("cars-raw-sync/", views.cars_raw_sync),
    path("cars-postgres-json/", views.cars_postgres_json),
    path("cars-pydantic/", views.cars_pydantic),
    path("cars-generated-field/", views.cars_generated_field),
    path("cars-generated-field-concat/", views.cars_generated_field_concat),
    path("json-sync/", views.json_sync),
    path("json-orjson-sync/", views.json_orjson_sync),
    path("json-msgspec-sync/", views.json_msgspec_sync),
    path("json-async/", views.json_async),
    path("json-orjson-async/", views.json_orjson_async),
    path("json-msgspec-async/", views.json_msgspec_async),
]

# For load-testing
urlpatterns += [
    path("cars/", views.cars_orjson_sync),
]
