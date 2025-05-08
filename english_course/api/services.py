import json
from functools import wraps

from django.http import JsonResponse

from english_course.models import User


def allow_methods(methods):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def require_access_to_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'No user_id in URL'}, status=400)

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        user = request.user

        if user.role == 'admin':
            kwargs['target_user'] = target_user
            return view_func(request, *args, **kwargs)

        if user.role == 'teacher' and target_user.teacher_id == user.id:
            kwargs['target_user'] = target_user
            return view_func(request, *args, **kwargs)

        if user.id == target_user.id:
            kwargs['target_user'] = target_user
            return view_func(request, *args, **kwargs)

        return JsonResponse({'error': 'Access denied'}, status=403)
    return wrapper

def require_elevated_role(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.user, 'role') or request.user.role not in roles:
                return JsonResponse({'error': 'Permission Denied'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def enforce_role_logic(view_func):

    VALID_ROLES = ['student', 'teacher']
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        user_role = getattr(request.user, 'role', None)
        if user_role not in ['admin', 'teacher']:
            return JsonResponse({'error': 'Permission Denied'}, status=403)

        role = 'student'
        teacher = None

        if user_role == 'admin':
            incoming_role = data.get('role', 'student')
            if incoming_role not in VALID_ROLES:
                return JsonResponse({'error': 'Permission Denied'}, status=403)
            role = incoming_role
        elif user_role == 'teacher':
            teacher = request.user

        kwargs['role'] = role
        kwargs['teacher'] = teacher
        return view_func(request, *args, **kwargs)
    return wrapper


