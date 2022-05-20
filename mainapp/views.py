from django.shortcuts import render
from authapp.models import HhUser, HhUserProfile


def index(request):
    """Главная страница"""
    context = {
        'title': 'Главная',
        'users': HhUser.objects.filter(),
        'accounts': HhUserProfile.objects.filter(),
    }
    return render(request, 'mainapp/index.html', context)
