from core.celery import app


# mock task to test celery
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
