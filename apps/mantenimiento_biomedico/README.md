# Módulo Mantenimiento Biomédico

Gestiona reportes de fallas de equipos biomédicos. Recibe mensajes desde Bonita vía RabbitMQ para crear y actualizar reportes automáticamente.

## Modelo

### Reporte

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK) | ID autoincremental |
| `descripcion_falla` | Text | Descripción de la falla reportada |
| `fecha_reporte` | DateTime | Fecha de creación (automática) |
| `estado` | String | `reportado`, `evaluado`, `reparado`, `reemplazado`, `sin_accion` |
| `isEvaluated` | Boolean | Indica si ya fue evaluado |
| `isRepairable` | Boolean | Indica si requiere reparación |
| `repairSuccessful` | Boolean | Indica si la reparación fue exitosa |
| `external_id` | String (único) | ID de correlación con Bonita |

## Endpoints

Todos bajo `/api/mantenimiento/`.

| Método | URL | Descripción |
|---|---|---|
| `GET` | `/reportes/` | Lista todos los reportes |
| `POST` | `/reportes/` | Crea un nuevo reporte |
| `GET` | `/reportes/{id}/` | Obtiene un reporte por ID |
| `PATCH` | `/reportes/{id}/` | Actualiza un reporte existente |

## RabbitMQ

Escucha la cola `mantenimiento_reporte`. Por cada mensaje JSON crea o actualiza un reporte según el `external_id`.

```bash
python manage.py consume_mantenimiento
```

## Documentación Swagger

`/swagger/mantenimiento/`
