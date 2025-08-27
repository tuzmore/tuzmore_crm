from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    # Custom role-based permission.
    # -Admin: Full access
    # - Manager: can view/create/update tasks & activities
    # - Sales: can only view their own and create

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)

        # Admin = Full access
        if role == 'admin':
            return True
        
        # Manager = read and write
        if role == 'manager' and request.method in['GET', 'POST', 'PUT', 'PATCH']:
            return True
        
        # Sales = can create and view only
        if role == 'sales' and request.method in ['GET', 'POST']:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', None)

        # Admon can access everything
        if role == 'admin':
            return True
        
        # Manager can access all tasks/activities
        if role == 'manager':
            return True
        
        # Sales can only see their own assigned tasks/activities
        if role == 'sales':
            return obj.assigned_to == request.user or obj.user == request.user
        return False