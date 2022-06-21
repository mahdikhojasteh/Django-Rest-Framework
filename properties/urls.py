from django.urls import path
from . import apis

urlpatterns = [
    path('', apis.PropertyListAPI.as_view()),
    path('fp', apis.PropertyPFListAPI.as_view()),
    path('<int:id>', apis.PropertyFetchAPI.as_view()),
    path('create', apis.PropertyCreateAPI.as_view()),
    path('update/<int:id>', apis.PropertyUpdateAPI.as_view()),
    path('delete/<int:id>', apis.PropertyDeleteAPI.as_view())
]
