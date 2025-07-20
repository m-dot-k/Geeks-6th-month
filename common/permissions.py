from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from datetime import date


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsAnonymous(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsStaff(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated or not request.user.is_staff:
            return False
        
        if request.method == 'POST':
            return False

        return True
    
class IsAdult(BasePermission):

    def has_permission(self, request, view):
        age = request.auth.get('age')
        if age is None or age < 18:
            raise PermissionDenied ("Возраст не указан или Вам должно быть 18 лет, чтобы создать продукт.")
        return super().has_permission(request, view)
