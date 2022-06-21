from django.db import models
from core.models import BaseModel


class Image(models.Model):
    extension = models.CharField(max_length=5)
    original_name = models.CharField(max_length=50)
    generated_name = models.CharField(max_length=50)


class Entity(models.Model):
    class entityEnum(models.IntegerChoices):
        unkown = 0
        comment = 1
        property = 2

    entity_id = models.PositiveIntegerField()
    entity_type = models.IntegerField(
        choices=entityEnum.choices, default=entityEnum.unkown)
    files = models.ManyToManyField(Image, through='FileEntity')


class FileEntity(BaseModel):
    files = models.ForeignKey(Image, on_delete=models.RESTRICT)
    entities = models.ForeignKey(Entity, on_delete=models.RESTRICT)
    is_deleted = models.BooleanField(default=False)
