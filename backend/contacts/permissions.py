from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    # Only Admin or Manager can create/delete Contacts
    # Sales users can read only.

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.role in ['admin', 'manager']
        return True
    

class IsOwnerOrReadOnly(BasePermission):
    # Users can edit their own contacts

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user or request.user.role in ['admin', 'manager']
        return True

