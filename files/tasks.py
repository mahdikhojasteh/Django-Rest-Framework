import os
import shutil
from core.celery import app
from celery import shared_task


# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

# mock task to test celery
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# @shared_task(bind=True)
@app.task(bind=True)
def move_files_task(self, source, destination):
    if source != destination:
        shutil.move(source, destination)
