from django.conf import settings
from django import template

register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(img_path):
    if not img_path:
        img_path = 'users_avatars/default.jpg'
    return f'{settings.MEDIA_URL}{img_path}'
