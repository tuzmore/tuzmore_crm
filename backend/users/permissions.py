from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
    

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'MANAGER'
    

class IsSales(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SALES'
