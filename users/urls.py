from django.urls import path
from users import apis

urlpatterns = [
    path('<int:id>', apis.GetUserByIdAPI.as_view()),
    path('list', apis.GetUsersAPI.as_view()),
    path('create', apis.CreateUserAPI.as_view()),
    path('create/superuser', apis.CreateSuperUserAPI.as_view()),
    path('<int:id>/update', apis.UpdateUserAPI.as_view()),
    path('<int:id>/sendotp', apis.Send_OTP_API.as_view()),
    path('<int:id>/veifyotp', apis.verify_OTP_API.as_view())
]