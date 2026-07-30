"""
Vistas para servir la documentación Swagger / OpenAPI 3.0 de Campaña de Vacunación
"""
import os
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

SWAGGER_JSON_PATH = os.path.join(os.path.dirname(__file__), 'swagger.json')

@csrf_exempt
def swagger_json_view(request):
    """Retorna el esquema OpenAPI 3.0 en formato JSON"""
    if os.path.exists(SWAGGER_JSON_PATH):
        with open(SWAGGER_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse(data)
    return JsonResponse({'error': 'Archivo swagger.json no encontrado'}, status=404)


@csrf_exempt
def swagger_ui_view(request):
    """Retorna la interfaz interactiva de Swagger UI"""
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Swagger UI - Campaña de Vacunación API</title>
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.18.3/swagger-ui.css" />
  <style>
    html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
    *, *:before, *:after { box-sizing: inherit; }
    body { margin:0; background: #fafafa; }
    .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.18.3/swagger-ui-bundle.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.18.3/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function() {
      const ui = SwaggerUIBundle({
        url: "/api/vacunacion/swagger.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
      });
      window.ui = ui;
    };
  </script>
</body>
</html>
    """
    return HttpResponse(html_content, content_type='text/html')
