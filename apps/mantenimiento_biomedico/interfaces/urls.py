from django.urls import path
from apps.mantenimiento_biomedico.interfaces.views import (
    EquipoView, ReporteView, EvalView,
    SolicitudView, EstimacionView,
    IntervView, CalibView, HistIntervView,
    RepDefectoView, EvalBPMView,
)

app_name = 'mantenimiento_biomedico'

urlpatterns = [
    path('equipos/', EquipoView.as_view(), name='eq_list'),
    path('equipos/<int:pk>/', EquipoView.as_view(), name='eq_detail'),
    path('equipos/<int:pk>/calibrar/', CalibView.as_view(), name='eq_calib'),
    path('equipos/<int:pk>/intervenciones/', HistIntervView.as_view(), name='eq_hist'),
    path('reportes/', ReporteView.as_view(), name='rep_list'),
    path('reportes/<int:pk>/', ReporteView.as_view(), name='rep_detail'),
    path('evaluaciones/', EvalView.as_view(), name='eval_list'),
    path('evaluaciones/<int:pk>/', EvalView.as_view(), name='eval_detail'),
    path('solicitudes/', SolicitudView.as_view(), name='sol_list'),
    path('solicitudes/<int:pk>/', SolicitudView.as_view(), name='sol_detail'),
    path('estimaciones/', EstimacionView.as_view(), name='est_list'),
    path('estimaciones/<int:pk>/', EstimacionView.as_view(), name='est_detail'),
    path('intervenciones/', IntervView.as_view(), name='interv_list'),
    path('bpm/rep-defecto/', RepDefectoView.as_view(), name='bpm_rep_defecto'),
    path('bpm/evaluar/', EvalBPMView.as_view(), name='bpm_evaluar'),
]
