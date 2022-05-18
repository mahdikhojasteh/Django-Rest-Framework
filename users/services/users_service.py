from django.contrib.auth import get_user_model
from users.models import User
from typing import Dict

def create_user(*, email: str, username: str, password: str=None):
    User = get_user_model()
    user = User(
        email=email,
        username=username
    )
    user.set_password(password)
    
    user.full_clean()
    user.save()
    
    return user

def create_superuser(*, email: str, username: str, password: str=None):
    user = create_user(
        email=email,
        username=username,
        password=password
    )
    user.is_admin = True
    user.full_clean()
    user.save()
    
    return user

def update_user(*, user:User, data:Dict) -> User:
    non_side_effect_fields = [
        'email',
        'username',
        'first_name',
        'last_name',
        'bio',
        'birthdate'
    ]
    
    has_updated = False
    
    for field in non_side_effect_fields:
        if field not in data:
            continue

        if not data[field]:
            continue

        if getattr(user, field) != data[field]:
            has_updated = True
            setattr(user, field, data[field])
    
    if has_updated:
        fields = non_side_effect_fields.copy()
        if 'password' in data and data['password']:
            user.set_password(data['password'])
            fields.append('password')
        user.full_clean()
        user.save(update_fields=fields)
    
    # Side-effect fields update here (e.g. username is generated based on first & last name)
    # ... some additional tasks with the user ...

    return user