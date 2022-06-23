from django.urls import path
from . import apis

urlpatterns = [
    path('', apis.SampleListAPI.as_view()),
    path('fp', apis.SamplePFListAPI.as_view()),
    path('<int:id>', apis.SampleFetchAPI.as_view()),
    path('create', apis.SampleCreateAPI.as_view()),
    path('update/<int:id>', apis.SampleUpdateAPI.as_view()),
    path('delete/<int:id>', apis.SampleDeleteAPI.as_view())
]
