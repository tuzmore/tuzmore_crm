from rest_framework import permissions

class DealPermission(permissions.BasePermission):
    """
    Role-based permissions for Deal model.
    - Admin: full access to all deals.
    - Manager: full access but only for team members' deals.
    - Sales: CRUD only on their own deals.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin: full access
        if user.role == "admin":
            return True

        # Manager: access if they are owner OR if the deal owner is in their team
        if user.role == "manager":
            # 🔑 Example check: team relation via `user.team.members`
            # Adjust this depending on your team model
            if obj.owner == user:
                return True
            if hasattr(user, "team") and obj.owner in user.team.members.all():
                return True
            return False

        # Sales: only access their own deals
        if user.role == "sales":
            return obj.owner == user

        return False
