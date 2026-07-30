from django.urls import path
from . import views

urlpatterns = [
    path(
        "medicamentos/",
        views.medicamentos,
        name="medicamentos",
    ),

    path(
        "medicamentos/<int:medicamento_id>/",
        views.medicamento,
        name="medicamento",
    ),
]