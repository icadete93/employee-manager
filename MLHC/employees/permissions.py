from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.security_level == 'M' or request.user.security_level == 'S':
            return True
        else:
            return request.user.username in request.get_full_path()

    def has_object_permission(self, request, view, obj):
        # if request.user.security_level == 'M' or request.user.security_level == 'S':
        #     return True
        if request.user.username == obj.employee.manager:
            return True
        else:
            return request.user.username in request.get_full_path()


class ManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.security_level == 'M' or request.user.security_level == 'S':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.security_level == 'M' or request.user.security_level == 'S':
            return True
        else:
            return False


class PasswordChangePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        pass