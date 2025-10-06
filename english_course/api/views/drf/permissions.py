from rest_framework.permissions import BasePermission

from english_course.models import User


class CanAccess(BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user

        if user == obj:
            return True

        if user.role == 'admin':
            return True

        if user.role == 'teacher':
            if isinstance(obj, User):
                return hasattr(obj, 'teacher') and obj.teacher == user

        if hasattr(obj, 'user'):
            return hasattr(obj.user, 'teacher' and obj.user.teacher == user)
