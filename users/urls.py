from django.urls import path
from users import views

urlpatterns = [
    path('<int:id>', views.GetUserByIdAPI.as_view()),
    path('list', views.GetUsersAPI.as_view()),
    path('create', views.CreateUserAPI.as_view()),
    path('create/superuser', views.CreateSuperUserAPI.as_view()),
    path('<int:id>/update', views.UpdateUserAPI.as_view())
]