from django.urls import path

from car import views

urlpatterns = [
    path("cars/", views.cars_hatchway_sync),
    # path("cars-async/", views.cars_hatchway_async),
]
