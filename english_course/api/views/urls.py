from django.urls import path

from english_course.api.views import *

app_name = 'api_english_course'

urlpatterns = [
    path('login/', api_login, name='api_login'),
    path('logout/', api_logout, name='api_logout'),
    path('users/', create_user_api, name='create_user_api'),
    path('profile/<int:user_id>', edit_user_profile, name='edit_other_user'),
    path('profile/<int:user_id>', get_user_profile, name='get_user_profile'),
    path('profile/', user_profile_view, name='get_user_profile'),
]