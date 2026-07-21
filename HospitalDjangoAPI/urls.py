from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/pruebas/', include('apps.pruebas_laboratorio.interfaces.urls')),
]
