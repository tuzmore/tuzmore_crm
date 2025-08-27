from rest_framework.permissions import BasePermission, SAFE_METHODS

class DealPermission(BasePermission):
    # Custom role-based permission for Deals.
    # - Admin full access.
    # -Manager can view and update all deals
    #  - Sales can only view/create/update their own deals

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            # admin has full access
            return True
        elif request.user.role == 'manager':
            return request.method in SAFE_METHODS or request.method in ['PUT', 'PATCH']
        elif request.user.role == 'sales':
            return obj.owner == request.user
        # only sales can access their deals
        return False