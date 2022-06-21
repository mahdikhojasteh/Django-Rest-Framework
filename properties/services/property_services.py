from typing import Dict, Any
from core.utils import model_update
from properties.models import Property
from rest_framework.exceptions import ValidationError


# keyword only arguments
def property_create(*, title: str, price: int) -> Property:
    property = Property(title=title, price=price)
    property.full_clean()
    property.save()

    return property


def property_update(*, property: Property, data: Dict[str, Any]) -> Property:
    property, has_updated = model_update(instance=property, data=data)
    # if not has_updated:
    #     raise ValidationError('model has not been updated')
    return property


def property_delete(*, property: Property):
    property.delete()
