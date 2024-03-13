from django.urls import path
from app.app_admin import views as admin_views
from app.user import views as user_views

urlpatterns = [
    path("v1/admin_login/", admin_views.login_admin, name = 'admin-login'),
    path("v1/login/", user_views.login_user, name= 'login-user'),
    path("v1/register/", user_views.register_user, name = 'register-user')
]
