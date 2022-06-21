from typing import List, Dict, Any, Tuple
from core.types import DjangoModelType
from rest_framework import serializers
from random import choice

# https://github.com/HackSoftware/Django-Styleguide


# style-guide model update
def model_update_sg(
    *,
    instance: DjangoModelType,
    fields: List[str],
    data: Dict[str, Any]
) -> Tuple[DjangoModelType, bool]:
    has_updated = False

    for field in fields:
        if field not in data:
            continue

        if getattr(instance, field) != data[field]:
            has_updated = True
            setattr(instance, field, data[field])

    if has_updated:
        instance.full_clean()
        instance.save(update_fields=fields)

    return instance, has_updated


# keyword only arguments
def model_update(
    *,
    instance: DjangoModelType,
    data: Dict[str, Any]
) -> Tuple[DjangoModelType, bool]:
    has_updated = False

    updated_fields = []
    for field in data.keys():
        if hasattr(instance, field):
            if getattr(instance, field) != data[field]:
                has_updated = True
                updated_fields.append(field)
                setattr(instance, field, data[field])
    if has_updated:
        instance.full_clean()
        instance.save(update_fields=updated_fields)

    return instance, has_updated


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def generate_random_code(length=6):
    seeds = 'e546d3bb410e44e68f2a2806ea3f2e97f31a8df0a2b942d99f76b1693075bcba'
    code_list = [choice(seeds) for i in range(length)]
    code = "".join(code_list)

    return code
