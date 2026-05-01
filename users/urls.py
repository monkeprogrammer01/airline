from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin-users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
]