from django.db import models
from rest_framework.exceptions import ValidationError


class Property(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.price < 10:
            raise ValidationError('price must be greater than 10')
