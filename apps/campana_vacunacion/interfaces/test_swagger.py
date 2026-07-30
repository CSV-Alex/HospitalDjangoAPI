"""
Tests para los endpoints de documentación Swagger / OpenAPI
"""
import os
import json
import unittest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HospitalDjangoAPI.settings')
django.setup()

from django.test import RequestFactory

from apps.campana_vacunacion.interfaces.swagger_views import (
    swagger_json_view,
    swagger_ui_view,
)


class TestSwaggerViews(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_swagger_json_view(self):
        """Test: Servir el esquema swagger.json"""
        request = self.factory.get('/api/vacunacion/swagger.json')
        response = swagger_json_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['openapi'], '3.0.3')
        self.assertIn('info', data)
        self.assertIn('paths', data)

    def test_swagger_ui_view(self):
        """Test: Servir la interfaz interactiva Swagger UI HTML"""
        request = self.factory.get('/api/vacunacion/swagger/')
        response = swagger_ui_view(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Swagger UI', content)
        self.assertIn('/api/vacunacion/swagger.json', content)


if __name__ == '__main__':
    unittest.main()
