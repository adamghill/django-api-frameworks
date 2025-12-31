from django.db.models import QuerySet
from djrest import ListCreateView

from car.forms import CarForm
from car.models import Car


class Cars(ListCreateView):
    model = Car
    form_class = CarForm

    def get_queryset(self):
        return Car.objects.with_annotations()


class CarsQuerysetToDict(ListCreateView):
    model = Car
    form_class = CarForm

    def serialize(self, obj_or_qs):
        if isinstance(obj_or_qs, QuerySet):
            result = list(obj_or_qs.as_dicts())

            # Rename formatted fields back to original names
            for item in result:
                if "created_at_formatted" in item:
                    item["created_at"] = item.pop("created_at_formatted")
                if "updated_at_formatted" in item:
                    item["updated_at"] = item.pop("updated_at_formatted")
            return result

        return super().serialize(obj_or_qs)
