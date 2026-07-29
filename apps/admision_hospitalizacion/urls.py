from django.urls import path
from . import views

urlpatterns = [
    path('api/ordenes/recepcionar/', views.recepcionar_orden, name='recepcionar_orden'),
    path('api/ordenes/<int:orden_id>/disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),
    path('api/ordenes/<int:orden_id>/validar-cobertura/', views.validar_cobertura, name='validar_cobertura'),
    path('api/ordenes/<int:orden_id>/iniciar-hospitalizacion/', views.iniciar_hospitalizacion, name='iniciar_hospitalizacion'),
    path('api/ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('api/hospitalizaciones/<int:hospitalizacion_id>/', views.obtener_hospitalizacion, name='obtener_hospitalizacion'),
]
