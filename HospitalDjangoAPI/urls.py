from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mantenimiento/', include('apps.mantenimiento_biomedico.interfaces.urls')),
]
