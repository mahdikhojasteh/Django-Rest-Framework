from django.contrib.auth import get_user_model


def get_users():
    User = get_user_model()
    return User.objects.all()

def get_user_by_id(*, id:int):
    User = get_user_model()
    user = User.objects.get(pk=id)
    return user