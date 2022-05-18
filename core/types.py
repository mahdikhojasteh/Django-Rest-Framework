from typing import TypeVar
from django.db import models

# Generic type for Django model
DjangoModelType = TypeVar('DjangoModelType', bound=models.Model)