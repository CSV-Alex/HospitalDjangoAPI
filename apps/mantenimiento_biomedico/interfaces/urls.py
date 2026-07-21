from django.urls import path
from apps.mantenimiento_biomedico.interfaces.views import EquipoView

app_name = 'mantenimiento_biomedico'

urlpatterns = [
    path('equipos/', EquipoView.as_view(), name='eq_list'),
    path('equipos/<int:pk>/', EquipoView.as_view(), name='eq_detail'),
]
