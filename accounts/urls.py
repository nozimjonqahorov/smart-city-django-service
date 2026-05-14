from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.MyPasswordChangeView.as_view(), name='password_change'),

    path('api/viloyatlar/', views.get_viloyatlar, name='api_viloyatlar'),
    path('api/tumanlar/<int:viloyat_id>/', views.get_tumanlar, name='api_tumanlar'),
]
