from django.contrib.auth.models import User
from django.db import transaction

from accounts.helpers.email import send_email_confirmation
from accounts.models import Profile


class UsernameAlreadyExists(Exception):
    pass


class EmailAlreadyExists(Exception):
    pass


def signup(username: str, password: str, email: str) -> User:
    if User.objects.filter(username=username).exists():
        raise UsernameAlreadyExists(username)

    if User.objects.filter(email=email).exists():
        raise EmailAlreadyExists(email)

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_active=False)
        Profile.objects.create(user=user)
        send_email_confirmation(user)
    return user


def discord_signup(username: str, email: str, discord_id: str) -> User:
    try:
        user = User.objects.get(profile__discord_id=discord_id)
    except User.DoesNotExist:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email)
            Profile.objects.create(user=user, discord_id=discord_id)
    return user
