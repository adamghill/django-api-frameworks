from django.urls import path

from car.views import Cars, CarsQuerysetToDict

urlpatterns = [
    path("cars-json/", Cars.as_view()),
    path("cars-queryset-as-dicts/", CarsQuerysetToDict.as_view()),
]

# For load-testing
urlpatterns += [
    path("cars/", Cars.as_view()),
]
