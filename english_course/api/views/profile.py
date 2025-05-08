import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from english_course.api.services import require_authenticated, require_access_to_user, allow_methods
from english_course.models import User, UserWord


@require_authenticated
@require_access_to_user
@allow_methods(['GET'])
def get_user_profile(request, user_id, target_user):
    return JsonResponse({
        'first_name': target_user.first_name,
        'last_name': target_user.last_name,
        'age': target_user.age,
        'email': target_user.email,
        'words': get_last_words(target_user),
    })

@require_authenticated
@allow_methods(['GET'])
def user_profile_view(request):
    user = request.user
    return JsonResponse({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email,
        'words': get_last_words(user),
    })


def get_last_words(user, count=10):
    return [
        {
            'word': uw.word.word,
            'translation': uw.translation
        }

        for uw in UserWord.objects.filter(user=user).order_by('-id')[:count]
    ]


@csrf_exempt
@allow_methods(['PUT'])
@require_authenticated
@require_access_to_user
def edit_user_profile(request, user_id, target_user):


    data = json.loads(request.body)

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    email = data.get('email')

    if not all([first_name, last_name, email]) or age is None:
        return JsonResponse({'error': 'Missing fields'}, status=400)

    if first_name.strip() == "" or last_name.strip() == "":
        return JsonResponse({'error': 'Empty first or last name'}, status=400)

    try:
        age = int(age)
        if age < 0 or age > 100:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid age'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error': 'Invalid email'}, status=400)

    target_user.first_name = first_name
    target_user.last_name = last_name
    target_user.age = age
    target_user.email = email
    target_user.save()

    return JsonResponse({
        'message': 'User profile updated',
        'user': {
            'first_name': target_user.first_name,
            'last_name': target_user.last_name,
            'age': target_user.age,
            'email': target_user.email,
        }
    })