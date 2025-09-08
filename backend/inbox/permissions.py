from rest_framework.permissions import BasePermission

class MessagePermission(BasePermission):
    """
    Role-based permission for Admin, Manager, Sales.
    """

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)

        # Allow if authenticated
        if not request.user.is_authenticated:
            return False

        # Admin = Full access
        if role == 'admin':
            return True

        # Manager = can view, create, update, delete
        if role == 'manager' and request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return True

        # Sales = can view and create only
        if role == 'sales' and request.method in ['GET', 'POST']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', None)

        if role == 'admin':
            return True

        if role == 'manager':
            return True

        if role == 'sales':
            # Sales can only access objects they own
            return (
                getattr(obj, 'assigned_to', None) == request.user or
                getattr(obj, 'user', None) == request.user or
                getattr(obj, 'sender', None) == request.user or
                getattr(obj, 'recipient', None) == request.user
            )

        return False
