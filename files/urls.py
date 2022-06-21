from django.urls import path
from files.apis import CreateFileAPI

urlpatterns = [
    path('create', CreateFileAPI.as_view())
]
