# BackendDjangoAPI - HospitalLINK

Equipo: HospitalLINK

Integrantes:
- Alex Enrique Cañapataña Vargas
- Berly Miuler Dueñas Mandamientos

Cliente: Hospital Honorio Delgado

Resumen
-------
Backend REST en Python (Django + Django REST Framework) que implementa los servicios necesarios para soportar tareas automáticas de procesos BPMN (orquestados por Bonitasoft). El sistema sigue principios de Domain‑Driven Design (DDD) y está diseñado como un servicio guiado por eventos que se comunica de forma asíncrona con el orquestador mediante RabbitMQ.

Visión general (qué y para quién)
-------------------------------
Este repositorio proporciona:
- Endpoints REST para registrar consultas ambulatorias y gestionar pacientes.
- Un consumer/publisher para integrar procesos BPMN con servicios internos a través de RabbitMQ.
- Documentación OpenAPI (Swagger) para probar y validar los servicios.

Stack
-----
- Lenguaje: Python
- Framework: Django / Django REST Framework
- Documentación OpenAPI: Swagger UI
- Mensajería: RabbitMQ
- Persistencia: SQLite / Django ORM
- Dependencias notables: Django, djangorestframework, pika

Estructura principal del repositorio
-----------------------------------

```text
apps/
  consultorio_externo/         # Módulo principal (DDD por capas)
    domain/                    # Entidades, ValueObjects, Factories, Exceptions
      entities.py
      value_objects.py
      factories.py
      exceptions.py
    application/               # Casos de uso / servicios de aplicación
      services.py              # RegistrarConsultaService
      consumers.py             # RabbitMQ consumer (integration)
    infrastructure/            # Acceso a infra (ORM, publisher)
      repositories.py
      rabbitmq_publisher.py    # Publicador que envía "true"/"false" en texto plano
    presentation/              # API (views + serializers)
      views.py                 # Endpoints REST y schemas Swagger
      serializers.py
    models.py                  # Models Django (Paciente ORM)
manage.py
requirements.txt
db.sqlite3                     # Base de datos
README.md
```

Flujo de ejecución
-------------------------------
1. Se recibe un mensaje desde Bonitasoft (o una llamada HTTP).
2. El consumer o el endpoint HTTP pasan los datos al servicio de aplicación `RegistrarConsultaService`.
3. El servicio usa el `PacienteFactory` para validar y construir la entidad `Paciente` (DDD).
4. Se persiste mediante el repositorio Django (infrastructure.repositories).
5. Se publica el resultado a RabbitMQ con el publicador `RabbitMQPublisher` como texto plano `"true"` o `"false"` (importante: Bonitasoft requiere texto literal).

Principales procesos y componentes
---------------------------------------------------
- Aplicación BPM: Se debe exponer como Application Page / Living Application en Bonitasoft y enlazar los conectores HTTP/RabbitMQ hacia este backend.
- Procesos de negocio: El proyecto está pensado para que las tareas automáticas (service tasks) llamen al endpoint o envíen mensajes a la cola `solicitud_consultorio`. Al terminar, se publica el resultado en `evento_consultorio_completado`.

Servicios REST (OpenAPI / Swagger)
---------------------------------
La API está documentada con OpenAPI y disponible en `/swagger/` al ejecutar el servidor.

Recursos principales:
1. Registrar consulta
   - Método: POST
   - URL: /api/consultorio/
   - Payload (ejemplo):
     ```json
     {
       "numeroHistoriaClinica": "HC-2026-001",
       "nombreCompleto": "Alex Canapatana",
       "fechaNacimiento": "1990-05-15",
       "necesitaExamen": true
     }
     ```
   - Comportamiento:
     - Valida usando Value Objects (NumeroHistoriaClinica, NombreCompleto, FechaNacimiento, NecesitaExamen).
     - Persiste el paciente.
     - Publica el resultado a RabbitMQ (mensaje texto: "true" o "false").
   - Respuestas:
     - 201: consulta registrada (devuelve necesita_examen y datos básicos)
     - 400: error de validación de dominio
     - 500: error interno

2. Listar pacientes
   - Método: GET
   - URL: /api/pacientes/
   - Respuesta: lista de pacientes con edad calculada

3. Obtener paciente por número de historia clínica
   - Método: GET
   - URL: /api/pacientes/{numero_historia_clinica}/
   - Respuesta: datos del paciente, edad calculada

Modelos relevantes
------------------
Entidad principal: Paciente (dominio y ORM)
- id (UUID interno)
- numero_historia_clinica (string)
- nombre_completo (string)
- fecha_nacimiento (date)
- necesita_examen (boolean)
- created_at / updated_at (timestamps en modelo ORM)

Integración con RabbitMQ (detalles importantes)
----------------------------------------------
- Producer (apps/consultorio_externo/infrastructure/rabbitmq_publisher.py)
  - Publica en la cola definida en la variable de settings `RABBITMQ_QUEUE_EVENTO_CONSULTORIO`.
  - POR COMPATIBILIDAD: publica el body como texto plano `"true"` o `"false"` (sin JSON) porque Bonitasoft interpreta arrays de strings a boolean con Boolean.valueOf().
- Consumer (apps/consultorio_externo/application/consumers.py)
  - Escucha la cola `solicitud_consultorio` y procesa mensajes JSON entrantes.

Ejemplos de uso (curl)
----------------------
Registrar consulta:
```bash
curl -X POST http://localhost:8000/api/consultorio/ \
  -H "Content-Type: application/json" \
  -d '{"numeroHistoriaClinica":"HC-2026-001","nombreCompleto":"Jose Garcia","fechaNacimiento":"1990-05-15","necesitaExamen":true}'
```

Buenas prácticas y pruebas
--------------------------
- Diseño orientado a DDD: `apps/consultorio_externo/domain` contiene Entities, ValueObjects, Factories y excepciones de dominio.
- Pruebas unitarias enfocadas en ValueObjects y Factories (TDD).
- Se aplicaron análisis estático (ej: SonarCloud) y se corrigieron defectos de severidad alta/critica. Quedan issues de menor prioridad (minor/info).
- Código organizado por capas: Presentation (views/serializers), Application (services/consumers), Domain (entities/value_objects), Infrastructure (repositories/publisher).

Ramas y control de versiones
----------------------------
Ramas principales (ejemplo):
- `main` — entrega final estable
- `development` — integración y estado actual (branch con información oficial)
- `feature/consultorios-externos-ddd-rabbitmq` — desarrollo del módulo consultorio externo

Referencias de código (dónde buscar)
------------------------------------
- Lógica de dominio y validaciones: `apps/consultorio_externo/domain/`
- Servicio de aplicación: `apps/consultorio_externo/application/services.py`
- Publicador RabbitMQ: `apps/consultorio_externo/infrastructure/rabbitmq_publisher.py`
- Endpoints y documentación Swagger: `apps/consultorio_externo/presentation/views.py`
- Modelos ORM: `apps/consultorio_externo/models.py`

Ejecución local
------------------------
Clonar, crear entorno, instalar dependencias, migrar y ejecutar:

```bash
git clone <url_del_repositorio>
cd HospitalDjangoAPI
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# configurar variables de entorno (o editar settings) para RabbitMQ si hace falta

python manage.py migrate
python manage.py runserver      # Swagger disponible en http://localhost:8000/swagger/
```

Ejecutar el consumidor (terminal aparte):
```bash
python manage.py consume_rabbitmq
```
(Requiere RabbitMQ corriendo y variables RABBITMQ_* configuradas).
