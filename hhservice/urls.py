from django.contrib import admin
from django.urls import path, include
from mainapp import views as mainapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('', mainapp.index, name='index'),
]
