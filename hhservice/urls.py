from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views as mainapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('', mainapp.index, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
