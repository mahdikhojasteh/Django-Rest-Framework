from typing import List, Dict, Any, Tuple
from core.types import DjangoModelType
from rest_framework import serializers

def model_update(
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

def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)

def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)
    
    if data is not None:
        return serializer_class(data=data, **kwargs)
    
    return serializer_class(**kwargs)