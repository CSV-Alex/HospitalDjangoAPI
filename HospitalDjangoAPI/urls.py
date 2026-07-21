from django.contrib import admin
from django.urls import path, include, include

urlpatterns = [
    path('', include('apps.admision_hospitalizacion.urls')),
    path('admin/', admin.site.urls),
    # path('api/mantenimiento/', include('apps.mantenimiento_biomedico.interfaces.urls')),
]