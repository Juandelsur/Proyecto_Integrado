# core/middleware.py
"""
Middleware para capturar el usuario actual en cada request
Permite que las signals accedan al usuario que realizó la acción
"""

import threading

# Thread-local storage para guardar el request actual
_thread_locals = threading.local()


def get_current_request():
    """
    Obtiene el request actual del thread-local storage
    Retorna None si no hay request activo
    """
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    """
    Obtiene el usuario del request actual
    Retorna None si no hay usuario autenticado
    """
    request = get_current_request()
    if request and hasattr(request, 'user'):
        return request.user if request.user.is_authenticated else None
    return None


class CurrentRequestMiddleware:
    """
    Middleware que guarda el request actual en thread-local storage
    Esto permite acceder al request desde cualquier parte del código,
    especialmente desde las signals de Django
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Guardar el request en thread-local
        _thread_locals.request = request
        
        try:
            response = self.get_response(request)
        finally:
            # Limpiar el thread-local después del request
            if hasattr(_thread_locals, 'request'):
                delattr(_thread_locals, 'request')
        
        return response