from rest_framework.permissions import BasePermission

# Only Admin or Manager can create/update/delete teams & assignments
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.role in ['ADMIN', 'MANAGER']
        return True
    
