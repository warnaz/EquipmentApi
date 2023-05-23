# from equapi.models import Equipment, TypeEquipment
from typing import List
from django.db.models import Model 


def get_models(model: Model, *args, **kwargs) -> List[Model]:
    result = model.objects.all().filter(*args, **kwargs)
    return list(result)

