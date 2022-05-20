from users.models import User
from typing import Dict
from core.utils import generate_random_code
from django.core.exceptions import ValidationError

def send_OTP(*, user: User):
    # keywork-only arguments
    # OTP -> One Time Password
    verify_code = generate_random_code()
    # TODO: 2022-05-20 17:10:47 Send OTP to user's mobile

    user.verify_code = verify_code
    user.full_clean()
    user.save(update_fields=['verify_code'])
    
    return user

def verify_OTP(*, user: User, code: str):
    if user.verify_code == code:
        user.mobile_verified = True
        user.full_clean()
        user.save(update_fields=['mobile_verified'])
    else:
        raise ValidationError(message='verification code does not match')
    
    return user


def create_user(*, username: str, mobile: str, password: str):
    
    user = User(
        username = username,
        mobile = mobile,
    )
    
    user.set_password(password)    
    user.full_clean()
    user.save()

    return user

def create_superuser(*, username: str, mobile: str, password: str):
    user = create_user(
        mobile=mobile,
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