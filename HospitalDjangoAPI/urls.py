from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.admision_hospitalizacion.urls')),
    path("api/", include("apps.farmacia.urls")),
    path('admin/', admin.site.urls),
    # path('api/mantenimiento/', include('apps.mantenimiento_biomedico.interfaces.urls')),
]