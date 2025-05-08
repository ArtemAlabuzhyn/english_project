import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from english_course.api.services import allow_methods, require_authenticated


@csrf_exempt
@allow_methods(['POST'])
def api_login(request):
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = str(data.get('username').strip())
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'username and password are required'}, status=400)
    password = str(password).strip()

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    login(request, user)
    return JsonResponse({'message': 'Login successful', 'username': user.username}, status=200)


@csrf_exempt
@allow_methods(['POST'])
@require_authenticated
def api_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)