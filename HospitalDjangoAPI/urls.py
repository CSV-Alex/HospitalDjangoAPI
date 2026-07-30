from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.mantenimiento_biomedico.interfaces.views import ReporteView

reporte_urls = [
    re_path(r'^api/mantenimiento/reportes/$', ReporteView.as_view(), name='reporte-list'),
    re_path(r'^api/mantenimiento/reportes/(?P<pk>\d+)/$', ReporteView.as_view(), name='reporte-detail'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="API Mantenimiento - Reportes",
        default_version='v1',
        description="Endpoints para crear, listar, obtener y actualizar reportes de mantenimiento.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=reporte_urls,
)

urlpatterns = [
    path('', include('apps.admision_hospitalizacion.urls')),
    path('admin/', admin.site.urls),
    path('api/mantenimiento/', include('apps.mantenimiento_biomedico.interfaces.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]