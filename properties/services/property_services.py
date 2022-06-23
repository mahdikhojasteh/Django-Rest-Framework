from typing import Dict, Any, MutableSequence
from core.utils import model_update
from properties.models import Property
from rest_framework.exceptions import ValidationError
from django.db import transaction
from files.services.file_services import FileStandardUploadService, file_delete_recycle


# keyword only arguments
def property_create(
    *,
    title: str,
    price: int,
    is_active: bool = True,
) -> Property:
    property = Property(title=title, price=price, is_active=is_active)
    property.full_clean()
    property.save()

    return property


@transaction.atomic
def property_image_create(
    *,
    property: Property,
    file_objs: MutableSequence[Any]
):
    for file_obj in file_objs:
        file_service = FileStandardUploadService(
            user=None,
            file_obj=file_obj
        )
        file = file_service.create()

        property.images.add(file)


def property_update(*, property: Property, data: Dict[str, Any]) -> Property:
    property, has_updated = model_update(instance=property, data=data)
    # if not has_updated:
    #     raise ValidationError('model has not been updated')
    return property


def property_delete(*, property: Property):
    for image in property.images.all():
        file_delete_recycle(instance=image)
    property.delete()
