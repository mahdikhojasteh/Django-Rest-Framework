from django.contrib.auth import get_user_model
from users.models import User


def get_users():
    User = get_user_model()
    return User.objects.all()

def get_user_by_id(*, id:int):
    User = get_user_model()
    # try:
    #     user = User.objects.get(pk=id)
    # except User.DoesNotExist as ex:
    #     raise ex
    user = User.objects.get(pk=id)
        
    return user

def user_get_login_data(*, user: User):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_admin': user.is_admin,
    }