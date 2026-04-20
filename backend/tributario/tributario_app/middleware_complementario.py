"""
Middleware complementario para tributario_app
Middleware adicional que no interfiere con el middleware principal
"""

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class MunicipioMiddleware(MiddlewareMixin):
    """
    Middleware para manejar el municipio en la sesión
    """
    
    def process_request(self, request):
        # Si no hay municipio en la sesión, establecer uno por defecto
        if 'empresa' not in request.session:
            request.session['empresa'] = '0301'
        
        # Agregar información del municipio al contexto de la request
        request.empresa = request.session.get('empresa', '0301')
        request.municipio_descripcion = self.obtener_descripcion_municipio(request.empresa)
    
    def obtener_descripcion_municipio(self, codigo):
        """
        Obtiene la descripción del municipio
        """
        municipios = {
            '0301': 'Municipio de Prueba',
            '0302': 'Municipio Secundario',
            '0303': 'Municipio Terciario'
        }
        return municipios.get(codigo, f'Municipio {codigo}')

class DebugMiddleware(MiddlewareMixin):
    """
    Middleware de debug para desarrollo
    """
    
    def process_request(self, request):
        # Solo en modo debug
        from django.conf import settings
        if settings.DEBUG:
            print(f"[DEBUG] Request: {request.method} {request.path}")
            print(f"[DEBUG] Session: {dict(request.session)}")
    
    def process_response(self, request, response):
        # Solo en modo debug
        from django.conf import settings
        if settings.DEBUG:
            print(f"[DEBUG] Response: {response.status_code}")
        return response

