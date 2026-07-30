from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Medicamento

import json


@csrf_exempt
def medicamentos(request):

    if request.method == "GET":
        medicamentos = Medicamento.objects.all()

        data = [
            {
                "id": medicamento.pk,
                "nombre": medicamento.nombre,
                "stock": medicamento.stock
            }
            for medicamento in medicamentos
        ]

        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)

        medicamento = Medicamento.objects.create(
            nombre=data["nombre"],
            stock=data["stock"]
        )

        return JsonResponse(
            {
                "id": medicamento.pk,
                "nombre": medicamento.nombre,
                "stock": medicamento.stock
            },
            status=201
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )


@csrf_exempt
def medicamento(request, medicamento_id):

    medicamento = get_object_or_404(Medicamento, pk=medicamento_id)

    if request.method == "GET":
        return JsonResponse({
            "id": medicamento.pk,
            "nombre": medicamento.nombre,
            "stock": medicamento.stock
        })

    elif request.method == "PUT":
        data = json.loads(request.body)

        medicamento.nombre = data["nombre"]
        medicamento.stock = data["stock"]
        medicamento.save()

        return JsonResponse({
            "id": medicamento.pk,
            "nombre": medicamento.nombre,
            "stock": medicamento.stock
        })

    elif request.method == "DELETE":
        medicamento.delete()

        return JsonResponse(
            {"message": "Medication deleted successfully"},
            status=200
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )