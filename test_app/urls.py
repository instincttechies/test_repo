from django.urls import path
from .import views

urlpatterns = [
    path('auth/login/', views.login_view, name='api-login'),
    path('auth/signup/', views.signup_view, name='api-signup'),
    path('auth/logout/', views.logout_view, name='api-logout'),
    path('dashboard/', views.dashboard, name='api-dashboard'),
    path('summary/', views.summary, name='api-summary'),
]