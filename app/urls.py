from django.urls import path
from app.app_admin import views as admin_views
from app.user import views as user_views
from app.question import views as question_views

urlpatterns = [

    path("v1/admin_login/", admin_views.login_admin, name = 'admin-login'),
    path("v1/user_login/", user_views.login_user, name= 'login-user'),
    path("v1/user_register/", user_views.register_user, name = 'register-user'),
    path("v1/verify_otp/", user_views.check_otp, name = 'check-otp'),
    path("v1/resend_otp/", user_views.resend_otp, name = "resend-otp"),
    path("v1/questions/<str:course_id>/", question_views.get_all_questions, name = "question-by-course"),
    path("v1/create_question/", question_views.create_question, name = "create-question"),
    path("v1/update_question/<str:question_id>/", question_views.update_question, name = "update-question"),
    path("v1/question/<str:id>/", question_views.get_question_by_question_id, name = "question")
]
