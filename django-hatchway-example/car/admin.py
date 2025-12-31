from django.contrib import admin

from car.models import Car, CarModel


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "make",
        "year",
        "color",
        "price",
        "created_at",
        "updated_at",
    ]
    search_fields = ["name", "make"]
    list_filter = ["year", "make", "color"]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["vin", "owner", "model", "created_at", "updated_at"]
    search_fields = ["vin", "owner"]
    list_filter = ["model", "created_at"]
    raw_id_fields = ["model"]
