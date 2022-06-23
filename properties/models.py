from django.db import models
from rest_framework.exceptions import ValidationError
from files.models import File


class Property(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    images = models.ManyToManyField(File, blank=True)

    def clean(self):
        if self.price < 30:
            raise ValidationError('price must be greater than 30')
