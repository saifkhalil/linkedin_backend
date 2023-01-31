"""linkedin_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers, permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib.auth import views as auth_views
from accounts.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    active_user,
    must_authenticate_view,
    send_active,
)

admin.site.site_header = 'Linkedin Backend'                    # default: "Django Administration"
admin.site.index_title = 'Linkedin Backend'                 # default: "Site administration"
admin.site.site_title = 'Linkedin Backend' # default: "Django site admin"

router = routers.DefaultRouter()

urlpatterns = [
    ## Admin URL
    path("admin/", admin.site.urls),

    ## API URLS
    path('api/', include(router.urls),name='apis'),
    path('api/', include('posts.urls'),name='posts'),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    # path('api/auth/', include('djoser.social.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    ## User Management 
    path('activate_user/<uidb64>/<token>', active_user, name='active'),
    path('admin/login/', auth_views.LoginView.as_view(), name="login"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'), name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/html_password_reset_email.html'),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
