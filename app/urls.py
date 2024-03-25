from django.urls import path
from app.app_admin import views as admin_views
from app.user import views as user_views
from app.course import views as course_views
from app.topic import views as topic_views
from app.sub_topic import views as sub_topic_views
from app.user_answer import user_views as user_answer_views
from app.question import views as question_views
from app.user_course_assignment import admin_views as admin_assignment_views
from app.user_course_assignment import user_views as user_assignment_views
from app.user_answer import admin_views as admin_answer_views
from app.gpt_review import admin_views as admin_gpt_views
from app.gpt_review import user_views as user_gpt_views

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
    # admin answer
    path("v1/admin/answers/", admin_answer_views.get_all_answer, name="admin-answers"),
    path("v1/admin/answer/<str:id>/", admin_answer_views.get_answer_by_id, name="admin-answer-by-id"),
    path("v1/admin/answer/assignment/<str:assign_id>/", admin_answer_views.get_answers_by_assignment, name="admin-answer-by-assignment"),
    path("v1/admin/answers/<str:user_id>/", admin_answer_views.get_answers_by_user, name="admin-users-answers"),
    # user-answer
    path("v1/add_answer/", user_answer_views.add_answer, name="add-answer"),
    path("v1/update_answer/<str:id>/", user_answer_views.update_answer, name="update-answer"),
    path("v1/user/answer_by_id/<str:id>/", user_answer_views.get_answer_by_id, name="answer_by_id"),
    path("v1/user/answers/", user_answer_views.get_answers_by_user, name="user-answers"),
    path("v1/user/answer/assignment/<str:assign_id>/", user_answer_views.get_answers_by_assignment, name="user-answer-by-assignment"),
    # user-course-assignment for admin
    path("v1/admin/assignments/", admin_assignment_views.get_all_assignments, name="admin-assignments"),
    path("v1/admin/assign_course/", admin_assignment_views.assign_course, name="admin-assign-course"),
    path("v1/admin/update_assign_course/<str:id>/", admin_assignment_views.update_assigned_course, name="admin-update-assign-course"),
    path("v1/admin/assignment/<str:id>/", admin_assignment_views.get_assignment_by_id, name="admin-assignment-by-id"),
    path("v1/admin/assignments/<str:user_id>/", admin_assignment_views.get_assignments_of_user, name='admin-user-assignments'),
    path("v1/admin/assignment/courses/<str:user_id>/", admin_assignment_views.get_user_assigned_courses, name="admin-assigned-courses"),
    path("v1/admin/assignment/<str:assign_id>/topics/", admin_assignment_views.get_assigned_topics, name="admin-assigned-topics"),
    path("v1/admin/assignment/<str:assign_id>/topic/<str:topic_id>/sub_topics/", admin_assignment_views.get_assigned_sub_topic, name="admin-assigned-sub-topics"),
    path("v1/admin/assignment/<str:assign_id>/questions/", admin_assignment_views.get_user_assigned_questions, name="admin-assigned-questions"),
    # user-course-assignment for user
    path("v1/user/assignments/", user_assignment_views.get_all_assignments, name="user-assignments"),
    path("v1/user/assignment/courses/", user_assignment_views.get_assigned_courses, name="user-assigned-courses"),
    path("v1/user/assignment/<str:assign_id>/", user_assignment_views.get_assignment_by_id, name="user-assignment-by-id"),
    path("v1/user/assignment/<str:assign_id>/topics/", user_assignment_views.get_assigned_topics_by_course, name="user-assigned-topics-by-course"),
    path("v1/user/assignment/<str:assign_id>/topic/<str:topic_id>/sub_topics/", user_assignment_views.get_assigned_sub_topics_by_topic, name="user-assigned-sub-topics-by-topic"),
    path("v1/user/assignment/<str:assign_id>/questions/", user_assignment_views.get_assigned_questions, name="user-assigned-questions"),
    # gpt-review
    path("v1/admin/gpt_review/<str:answer_id>", admin_gpt_views.get_gpt_review_by_answer, name="admin-get-gpt-review-by-answer-id"),
    path("v1/user/gpt_review/<str:answer_id>", user_gpt_views.get_gpt_review_by_answer, name="user-get-gpt-review-by-answer-id"),
]
