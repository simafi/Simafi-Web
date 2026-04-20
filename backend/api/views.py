from django.shortcuts import render
from django.http import JsonResponse

def api_home(request):
    """Vista principal de la API"""
    return JsonResponse({{
        'status': 'success',
        'message': 'API del Sistema Municipal Modular',
        'version': '1.0.0'
    }})

def api_health(request):
    """Vista de salud de la API"""
    return JsonResponse({{
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z'
    }})
