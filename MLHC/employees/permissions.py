from rest_framework import permissions


class EmployeePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.is_admin == request.user.is_admin
    # has_object_permission(self, request, view, obj)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if obj.owner:
            # return obj.owner == request.user
        # else:
            return obj.user == request.user
