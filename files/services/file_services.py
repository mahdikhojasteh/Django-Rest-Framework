import mimetypes
import os
from pathlib import Path
from typing import Tuple, Dict, Any

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from files.models import File
from files.utils import (
    file_generate_upload_path,
    file_generate_local_upload_url,
    file_generate_name,
    bytes_to_mib
)

from users.models import User as BaseUser
from files.tasks import move_files_task


def _validate_file_size(file_obj):
    max_size = settings.FILE_MAX_SIZE

    if file_obj.size > max_size:
        raise ValidationError(
            f"File is too large. It should not exceed {bytes_to_mib(max_size)} MiB")


@transaction.atomic
def file_delete_recycle(*, instance: File) -> File:
    label = 'recycled'
    old_name = instance.file.name
    # 'files/5b3b31a64c764fac86a22cb080ed596b.jpg'

    file_name = old_name.split(os.path.sep)[1:][0]
    # '5b3b31a64c764fac86a22cb080ed596b.jpg'

    new_name = os.path.join(label, file_name)
    # 'recycled/5b3b31a64c764fac86a22cb080ed596b.jpg'

    old_path = os.path.join(settings.MEDIA_ROOT, old_name)
    new_path = os.path.join(settings.MEDIA_ROOT, new_name)

    Path(settings.MEDIA_ROOT, label).mkdir(parents=True, exist_ok=True)

    move_files_task.delay(str(old_path), str(new_path))
    # move_files_task.apply_async(kwargs={'source': old_path.resolve(
    # ), 'destination': new_path.resolve()}, countdown=60)

    instance.file.name = new_name
    instance.is_deleted = True

    instance.full_clean()
    instance.save(update_fields=['file', 'is_deleted'])

    return instance


class FileStandardUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates 2 different behaviors (create & update) under a namespace.

    Meaning, we use the class here for:

    1. The namespace
    2. The ability to reuse `_infer_file_name_and_type` (which can also be an util)
    """

    def __init__(self, user: BaseUser, file_obj):
        self.user = user
        self.file_obj = file_obj

    def _infer_file_name_and_type(self, file_name: str = "", file_type: str = "") -> Tuple[str, str]:
        if not file_name:
            file_name = self.file_obj.name

        if not file_type:
            guessed_file_type, encoding = mimetypes.guess_type(file_name)

            if guessed_file_type is None:
                file_type = ""
            else:
                file_type = guessed_file_type

        return file_name, file_type

    @transaction.atomic
    def create(self, file_name: str = "", file_type: str = "") -> File:
        _validate_file_size(self.file_obj)

        file_name, file_type = self._infer_file_name_and_type(
            file_name, file_type)

        obj = File(
            file=self.file_obj,
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            upload_finished_at=timezone.now()
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def update(self, file: File, file_name: str = "", file_type: str = "") -> File:
        _validate_file_size(self.file_obj)

        file_name, file_type = self._infer_file_name_and_type(
            file_name, file_type)

        file.file = self.file_obj
        file.original_file_name = file_name
        file.file_name = file_generate_name(file_name)
        file.file_type = file_type
        file.uploaded_by = self.user
        file.upload_finished_at = timezone.now()

        file.full_clean()
        file.save()

        return file


class FileDirectUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates a flow (start & finish) + one-off action (upload_local) into a namespace.

    Meaning, we use the class here for:

    1. The namespace
    """

    def __init__(self, user: BaseUser):
        self.user = user

    @transaction.atomic
    def start(self, *, file_name: str, file_type: str) -> Dict[str, Any]:
        file = File(
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            file=None
        )
        file.full_clean()
        file.save()

        upload_path = file_generate_upload_path(file, file.file_name)

        """
        We are doing this in order to have an associated file for the field.
        """
        file.file = file.file.field.attr_class(
            file, file.file.field, upload_path)
        file.save()

        presigned_data: Dict[str, Any] = {}

        # if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
        #     presigned_data = s3_generate_presigned_post(
        #         file_path=upload_path, file_type=file.file_type
        #     )

        # else:
        #     presigned_data = {
        #         "url": file_generate_local_upload_url(file_id=str(file.id)),
        #     }
        presigned_data = {
            "url": file_generate_local_upload_url(file_id=str(file.id)),
        }

        return {"id": file.id, **presigned_data}

    @transaction.atomic
    def finish(self, *, file: File) -> File:
        # Potentially, check against user
        file.upload_finished_at = timezone.now()
        file.full_clean()
        file.save()

        return file

    @transaction.atomic
    def upload_local(self, *, file: File, file_obj) -> File:
        _validate_file_size(file_obj)

        # Potentially, check against user
        file.file = file_obj
        file.full_clean()
        file.save()

        return file
