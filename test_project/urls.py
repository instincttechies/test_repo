from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('summary/', TemplateView.as_view(template_name='summary.html'), name='summary'),
    path('api/', include('test_app.urls')),
]
