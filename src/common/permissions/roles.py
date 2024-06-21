from rest_framework import permissions

class IsAuthAndRoles(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios con roles específicos.
    """

    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado y si su rol está en la lista de roles permitidos
        return bool(request.user and request.user.is_authenticated and request.user.role in self.allowed_roles)
