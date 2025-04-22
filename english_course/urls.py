from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'english_course'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.user_profile, name='user'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('add_word/<int:user_id>', views.add_word, name='add_word'),
    path('edit_word/<int:word_id>/', views.edit_word, name='edit_word'),
    path('delete_userword/<int:word_id>/', views.delete_userword, name='delete_userword'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='english_course:login'), name='logout'),
    path('create_user/', views.create_user, name='create_user'),
    path('vocabulary/<int:user_id>/', views.full_vocabulary, name='full_vocabulary'),
]