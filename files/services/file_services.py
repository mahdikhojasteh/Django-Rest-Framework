from files.models import File, Entity, FileEntity
from typing import Dict
import uuid
from pathlib import Path
from django.conf import settings


def createFile(*, extension: str,
               original_name: str,
               generated_name: str,
               entity_id: int,
               entity_type: int):
    # file = File(extension=extension,
    #             original_name=original_name
    #             generated_name=)

    pass


def deleteFile():
    pass


def generateFilePath(filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}{ext}'

    return Path(settings.MEDIA_ROOT, filename).absolute()
