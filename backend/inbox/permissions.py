from rest_framework import permissions

class IsAdminUserReadOnly(permissions.BasePermission):
    """
    Only admin users can view the messages.
    Anyone can create (POST) messages.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True  # anyone can send message
        return request.user and request.user.is_staff
