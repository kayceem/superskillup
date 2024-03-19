from django.urls import path
from app.app_admin import views as admin_views
from app.user import views as user_views
from app.course import views as course_views
from app.topic import views as topic_views

urlpatterns = [
    path("v1/admin_login/", admin_views.login_admin, name='admin-login'),
    path("v1/user_login/", user_views.login_user, name='login-user'),
    path("v1/user_register/", user_views.register_user, name='register-user'),
    path("v1/verify_otp/", user_views.check_otp, name='check-otp'),
    path("v1/resend_otp/", user_views.resend_otp, name='resend-otp'),
    path("v1/create_course/", course_views.create_course, name='create-course'),
    path("v1/update_course/<str:id>", course_views.update_course, name='update-course'),
    path("v1/course/", course_views.get_all_courses, name='search-get-all-courses'),
    path("v1/course/<str:id>", course_views.get_course_by_id, name='get-course-by-id'),
    path("v1/create_topic/", topic_views.create_topic, name='create-topic'),
    path("v1/update_topic/<str:id>", topic_views.update_topic, name='update-topic'),
    path("v1/topic/course/<str:id>", topic_views.get_topics_by_course, name='get-topics-by-course'),
    path("v1/topic/<str:id>", topic_views.get_topic_by_id, name='get-topic-by-id'),
]
