from importlib.resources import path
from pathlib import Path
from uuid import uuid4


def file_generate_name(original_file_name):
    extension = Path(original_file_name).suffix

    return f'{uuid4().hex}{extension}'


def file_generate_upload_path(instance):
    return f'files/{instance.file_name}'
