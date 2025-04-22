from .models import User


def get_allowed_user_or_redirect(request_user, target_user_id):
    try:
        target_user = User.objects.get(pk=target_user_id)
    except User.DoesNotExist:
        return None

    if request_user.role == 'admin':
        return target_user

    if request_user.role == 'teacher' and target_user.teacher_id == request_user.id:
        return target_user

    if request_user.role == 'student' and request_user.id == target_user_id:
        return target_user

    if request_user.id == target_user_id:
        return target_user

    return None
