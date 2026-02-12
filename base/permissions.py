from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow users with 'admin' role to access the API.
    """
    
    def has_permission(self, request, view):
        """
        Return True if user is authenticated and has 'admin' role.
        """
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user has 'admin' role
        return request.user.role == 'admin'
