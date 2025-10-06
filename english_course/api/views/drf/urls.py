from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

# from english_course.api.views.drf.auth import LoginAPIView, LogoutAPIView
from english_course.api.views.drf.profile import UserProfileAPIView, UserDetailAPIView
from english_course.api.views.drf.users import UserCreateAPIView
from english_course.api.views.drf.words import WordsView, WordDetailView
urlpatterns = [
    # path('login/', LoginAPIView.as_view(), name='drf_login'),
    # path('logout/', LogoutAPIView.as_view(), name='drf_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileAPIView.as_view(), name='drf_user_profile'),
    path('profile/<int:pk>/', UserDetailAPIView.as_view(), name='user_edit'),
    path('register/', UserCreateAPIView.as_view(), name='drf_register'),
    path('words/', WordsView.as_view(), name='words'),
    path('words/<int:pk>/', WordDetailView.as_view(), name='word_detail')
]


