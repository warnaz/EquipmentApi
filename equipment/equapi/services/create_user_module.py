from django.contrib.auth.models import User


def user_create(username, password, **kwargs):
    instance = User.objects.create(username=username)
    instance.set_password(password)
    return instance
