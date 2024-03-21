from django.urls import path
from app.app_admin import views as admin_views
from app.user import views as user_views
from app.course import views as course_views
from app.topic import views as topic_views
from app.sub_topic import views as sub_topic_views
from app.user_answer import views as user_answer_views
from app.question import views as question_views
from app.user_course_assignment import admin_views as admin_assignment_views

urlpatterns = [
    # login
    path("v1/admin_login/", admin_views.login_admin, name='admin-login'),
    path("v1/user_login/", user_views.login_user, name='login-user'),
    path("v1/user_register/", user_views.register_user, name='register-user'),
    path("v1/verify_otp/", user_views.check_otp, name='check-otp'),
    path("v1/resend_otp/", user_views.resend_otp, name='resend-otp'),
    # courses
    path("v1/create_course/", course_views.create_course, name='create-course'),
    path("v1/update_course/<str:id>", course_views.update_course, name='update-course'),
    path("v1/course/", course_views.get_all_courses, name='get-all-courses'),
    path("v1/course/<str:id>", course_views.get_course_by_id, name='get-course-by-id'),
    # topics
    path("v1/create_topic/", topic_views.create_topic, name='create-topic'),
    path("v1/update_topic/<str:id>", topic_views.update_topic, name='update-topic'),
    path("v1/topic/course/<str:id>", topic_views.get_topics_by_course, name='get-topics-by-course'),
    path("v1/topic/<str:id>", topic_views.get_topic_by_id, name='get-topic-by-id'),
    # sub-topics
    path("v1/create_sub_topic/", sub_topic_views.create_sub_topic, name='create-sub-topic'),
    path("v1/update_sub_topic/<str:id>", sub_topic_views.update_sub_topic, name='update-sub-topic'),
    path("v1/sub_topic/topic/<str:id>", sub_topic_views.get_sub_topics_by_topic, name='get-sub-topics-by-topic'),
    path("v1/sub_topic/<str:id>", sub_topic_views.get_sub_topic_by_id, name='get-sub-topic-by-id'),
    # question
    path("v1/questions/<str:course_id>/", question_views.get_all_questions, name="question-by-course"),
    path("v1/create_question/", question_views.create_question, name="create-question"),
    path("v1/update_question/<str:question_id>/", question_views.update_question, name="update-question"),
    path("v1/question/<str:id>/", question_views.get_question_by_id, name="question"),
    # user-answer
    path("v1/add_answer/", user_answer_views.add_answer, name="add-answer"),
    path("v1/answer_by_user/", user_answer_views.get_answer_by_user_id, name="user-answer-by-user-id"),
    path("v1/update_answer/<str:id>/", user_answer_views.update_answer, name="update-answer"),
    path("v1/answer_by_id/<str:id>/", user_answer_views.get_answer_by_id, name='answer-by-id'),
    # user-course-assignment for admin
    path("v1/assign_course/", admin_assignment_views.assign_course, name="assign-course"),
    path("v1/assignments/", admin_assignment_views.get_all_assignments, name="assignments"),
    path("v1/assignment/<str:id>/", admin_assignment_views.get_assignment_by_id, name="assignment-by-id"),
    path("v1/assignment/courses/<str:user_id>/", admin_assignment_views.get_user_assigned_courses, name="assigned-courses"),
    path("v1/assignment/topics/<str:assign_id>/", admin_assignment_views.get_assigned_topics, name="assigned-topics"),
    path("v1/update_assign_course/<str:id>/", admin_assignment_views.update_assigned_course, name="update-assign-course"),
    path("v1/assignments/<str:user_id>/", admin_assignment_views.get_assignments_of_user, name='user-assignments'),
    path("v1/assignment/<str:assign_id>/sub_topics/<str:topic_id>/", admin_assignment_views.get_assigned_sub_topic, name="assigned-sub-topics"),
    path("v1/assignment/questions/<str:assign_id>/", admin_assignment_views.get_user_assigned_questions, name="assigned-questions"),
]
