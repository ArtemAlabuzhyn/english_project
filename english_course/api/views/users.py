import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from english_course.api.services import allow_methods, require_elevated_role, enforce_role_logic
from english_course.models import User


@csrf_exempt
@login_required
@require_elevated_role(['admin', 'teacher'])
@enforce_role_logic
@allow_methods(['POST'])
def create_user_api(request):


    data = json.loads(request.body)
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not all([username, password1, password2, first_name, last_name]):
        return JsonResponse({'error': 'Missing fields'}, status=400)

    if password1 != password2:
        return JsonResponse({'error': 'Passwords do not match'}, status=400)


    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=409)

    role = 'student'

    if request.user.role == 'admin':
        role = data.get('role', 'student')


    # teacher = request.user if request.user.role == 'teacher' else None
    teacher = None

    user = User.objects.create_user(
        username=username,
        password=password1,
        first_name=first_name,
        last_name=last_name,
        role=role,
        teacher=teacher
    )

    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
    }, status=201)