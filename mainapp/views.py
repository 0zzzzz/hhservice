from django.shortcuts import render
from authapp.models import HhUser


def index(request):
    context = {
        'title': 'Главная',
        'users': HhUser.objects.filter(),
    }
    return render(request, 'mainapp/index.html', context)
