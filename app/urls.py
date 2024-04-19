from django.urls import path
from app.app_admin import views as admin_views
from app.user import views as user_views
from app.course import views as course_views
from app.topic import views as topic_views
from app.sub_topic import views as sub_topic_views
from app.question_answer import user_views as user_answer_views
from app.question import views as question_views
from app.user_course_enrollment import admin_views as admin_enrollment_views
from app.user_course_enrollment import user_views as user_enrollment_views
from app.question_answer import admin_views as admin_answer_views
from app.gpt_review import admin_views as admin_gpt_views
from app.gpt_review import user_views as user_gpt_views
from app.manager_feedback import views as manager_feedback
from app.user_course_enrollment import search as search_views
from app.assignment import views as assignment_views
from app.user_assignment import user_views as user_assignment_views
from app.user_assignment import admin_views as admin_user_assignment_views
from app.user_assignment_submission import admin_views as admin_user_assignment_submission_views
from app.user_assignment_submission import user_views as user_assignment_submission_views
from app.tag import views as tag_views

urlpatterns = [
    # login
    path("v1/admin/login/", admin_views.login_admin, name='admin-login'),
    path("v1/admin/user/", user_views.get_all_users, name='get-all-users'),
    path("v1/user/login/", user_views.login_user, name='login-user'),
    path("v1/user/register/", user_views.register_user, name='register-user'),
    path("v1/user/verify-otp/", user_views.check_otp, name='check-otp'),
    path("v1/user/resend-otp/", user_views.resend_otp, name='resend-otp'),
    path("v1/user/verify-otp-forgot-password/", user_views.check_otp_forgot_password, name='check-otp-forgot-password'),
    path("v1/user/forgot-password/", user_views.forgot_password, name='forgot-password'),
    path("v1/user/otp/", user_views.send_otp_forgot_password, name='otp'),
    path("v1/user/", user_views.get_user_info, name='get-user'),
    # courses
    path("v1/admin/course/create/", course_views.create_course, name='create-course'),
    path("v1/admin/course/update/<str:id>/", course_views.update_course, name='update-course'),
    path("v1/admin/course/delete/<str:id>/", course_views.delete_course, name='delete-course'),
    path("v1/admin/course/", course_views.get_all_courses, name='get-all-courses'),
    path("v1/admin/course/<str:id>/", course_views.get_course_by_id, name='get-course-by-id'),
    # topics
    path("v1/admin/topic/create/", topic_views.create_topic, name='create-topic'),
    path("v1/admin/topic/update/<str:id>/", topic_views.update_topic, name='update-topic'),
    path("v1/admin/topic/delete/<str:id>/", topic_views.delete_topic, name='delete-topic'),
    path("v1/admin/topic/course/<str:course_id>/", topic_views.get_topics_by_course, name='get-topics-by-course'),
    path("v1/admin/topic/<str:id>/", topic_views.get_topic_by_id, name='get-topic-by-id'),
    # sub-topics
    path("v1/admin/sub-topic/create/", sub_topic_views.create_sub_topic, name='create-sub-topic'),
    path("v1/admin/sub-topic/update/<str:id>/", sub_topic_views.update_sub_topic, name='update-sub-topic'),
    path("v1/admin/sub-topic/delete/<str:id>/", sub_topic_views.delete_sub_topic, name='delete-sub-topic'),
    path("v1/admin/sub-topic/topic/<str:topic_id>/", sub_topic_views.get_sub_topics_by_topic, name='get-sub-topics-by-topic'),
    path("v1/admin/sub-topic/<str:id>/", sub_topic_views.get_sub_topic_by_id, name='get-sub-topic-by-id'),
    # question
    path("v1/admin/question/create/", question_views.create_question, name="create-question"),
    path("v1/admin/question/update/<str:id>/", question_views.update_question, name="update-question"),
    path("v1/admin/question/delete/<str:id>/", question_views.delete_question, name="delete-question"),
    path("v1/admin/question/<str:id>/", question_views.get_question_by_id, name="get-questions-by-id"),
    path("v1/admin/question/course/<str:course_id>/", question_views.get_questions_by_course, name="get-questions-by-course"),
    path("v1/admin/question/sub-topic/<str:sub_topic_id>/", question_views.get_questions_by_sub_topic, name="get-questions-by-sub-topic"),
    # assignments
    path("v1/admin/assignment/create/", assignment_views.create_assignment, name='create-assignment'),
    path("v1/admin/assignment/update/<str:id>/", assignment_views.update_assignment, name='update-assignment'),
    path("v1/admin/assignment/delete/<str:id>/", assignment_views.delete_assignment, name='delete-assignment'),
    path("v1/admin/assignment/course/<str:course_id>/", assignment_views.get_assignments_by_course, name='get-assignments-by-course'),
    path("v1/admin/assignment/<str:id>/", assignment_views.get_assignment_by_id, name='get-assignment-by-id'),
    # user-course-enrollment for admin
    path("v1/admin/enrollment/", admin_enrollment_views.get_all_enrollments, name="admin-get-all-enrollments"),
    path("v1/admin/enrollment/create/", admin_enrollment_views.create_user_course_enrollment, name="admin-create-user-course-enrollment"),
    path("v1/admin/enrollment/update/<str:id>/", admin_enrollment_views.update_user_course_enrollment, name="admin-update-user-course-enrollment"),
    path("v1/admin/enrollment/delete/<str:id>/", admin_enrollment_views.delete_user_course_enrollment, name="admin-delete-user-course-enrollment"),
    path("v1/admin/enrollment/user/", admin_enrollment_views.get_enrolled_users, name="admin-get-enrolled_users"),
    path("v1/admin/enrollment/user/<str:user_id>/", admin_enrollment_views.get_user_enrollments, name='admin-get-user-enrollments'),
    path("v1/admin/enrollment/user/<str:user_id>/course/", admin_enrollment_views.get_user_enrolled_courses, name="admin-get-user-enrolled-courses"),
    path("v1/admin/enrollment/<str:id>/", admin_enrollment_views.get_enrollment_by_id, name="admin-get-enrollment-by-id"),
    # user-course-enrollment for user
    path("v1/user/enrollment/", user_enrollment_views.get_all_enrollments, name="user-get-all-enrollments"),
    path("v1/user/enrollment/manager/", user_enrollment_views.get_managers_of_user, name="user-get-managers-of-user"),
    path("v1/user/enrollment/course/", user_enrollment_views.get_enrolled_courses, name="user-get-enrolled-courses"),
    path("v1/user/enrollment/<str:id>/", user_enrollment_views.get_enrollment_by_id, name="user-get-enrollment-by-id"),
    path("v1/user/enrollment/<str:id>/topic/", user_enrollment_views.get_enrolled_topics, name="user-get-enrolled-topics"),
    path("v1/user/enrollment/<str:id>/topic/<str:topic_id>/sub-topic/", user_enrollment_views.get_enrolled_sub_topics, name="user-get-enrolled-sub-topics"),
    path("v1/user/enrollment/<str:id>/sub-topic/<str:sub_topic_id>/question/", user_enrollment_views.get_enrolled_questions, name="user-get-enrolled-questions"),
    # user-assignments for admin
    path("v1/admin/user-assignment/create/", admin_user_assignment_views.create_user_assignment, name="admin-create-user-assignment"),
    path("v1/admin/user-assignment/update/<str:id>/", admin_user_assignment_views.update_user_assignment, name="admin-update-user-assignment"),
    path("v1/admin/user-assignment/user/<str:user_id>/", admin_user_assignment_views.get_all_user_assignments_by_user, name='admin-get-all-user-assignments-by-user'),
    path("v1/admin/user-assignment/course/<str:course_id>/", admin_user_assignment_views.get_all_user_assignments_by_course, name='admin-get-all-user-assignments-by-course'),
    path("v1/admin/user-assignment/enrollment/<str:enrollment_id>/", admin_user_assignment_views.get_user_assignments_by_enrollment, name='admin-get-user-assignments-by-enrollment'),
    path("v1/admin/user-assignment/user/<str:user_id>/course/<str:course_id>/", admin_user_assignment_views.get_user_assignments_by_course, name='admin-get-user-assignment-by-course'),
    path("v1/admin/user-assignment/<str:id>/", admin_user_assignment_views.get_user_assignment_by_id, name='admin-get-user-assignment-by-id'),
    # user-assignments for admin
    path("v1/user/user-assignment/", user_assignment_views.get_all_user_assignments, name='user-get-all-user-assignments'),
    path("v1/user/user-assignment/course/<str:course_id>/", user_assignment_views.get_user_assignments_by_course, name='user-get-user-assignments-by-course'),
    path("v1/user/user-assignment/enrollment/<str:enrollment_id>/", user_assignment_views.get_user_assignments_by_enrollment, name='user-et-user-assignments-by-enrollment'),
    path("v1/user/user-assignment/<str:id>/", user_assignment_views.get_user_assignment_by_id, name='user-get-user-assignment-by-id'),
    # user-assignment-submission for admin
    path("v1/admin/assignment-submission/user-assignment/<str:user_assignment_id>/", admin_user_assignment_submission_views.get_user_assignment_submission_by_user_assignment, name='admin-get-assignment-submission-by-user-assignment'),
    path("v1/admin/assignment-submission/<str:id>/", admin_user_assignment_submission_views.get_user_assignment_submission_by_id, name='admin-get-assignment-submission-by-id'),
    # user-assignment-submission for user
    path("v1/user/assignment-submission/create/", user_assignment_submission_views.add_assignment_submission, name="user-add-assignment-submission"),
    path("v1/user/assignment-submission/update/<str:id>/", user_assignment_submission_views.update_assignment_submission, name="user-update-assignment-submission"),
    path("v1/user/assignment-submission/user-assignment/<str:user_assignment_id>/", user_assignment_submission_views.get_user_assignment_submission_by_user_assignment, name='user-get-assignment-submmsion-by-user-assignment'),
    path("v1/user/assignment-submission/<str:id>/", user_assignment_submission_views.get_user_assignment_submission_by_id, name="user-get-assignment-submission-by-id"),
    # user-answer
    path("v1/user/answer/create/", user_answer_views.add_answer, name="user-add-answer"),
    path("v1/user/answer/update/<str:id>/", user_answer_views.update_answer, name="user-update-answer"),
    path("v1/user/answer/<str:id>/", user_answer_views.get_answer_by_id, name="user-get-answer-by-id"),
    path("v1/user/answer/question/<str:question_id>/", user_answer_views.get_answer_by_question, name="user-get-answer-by-question"),
    # admin answer
    path("v1/admin/answer/question/<str:question_id>/user/<str:user_id>/", admin_answer_views.get_answer_by_question, name="get-answer-by-question"),
    path("v1/admin/answer/<str:id>/", admin_answer_views.get_answer_by_id, name="admin-get-answer-by-id"),
    # gpt-review
    path("v1/admin/gpt-review/<str:answer_id>/", admin_gpt_views.get_gpt_review_by_answer, name="admin-get-gpt-review-by-answer-id"),
    path("v1/user/gpt-review/<str:answer_id>/", user_gpt_views.get_gpt_review_by_answer, name="user-get-gpt-review-by-answer-id"),
    # admin-review
    path("v1/admin/review/create/", manager_feedback.add_manager_feedback, name="admin-add-manager-feedback"),
    path("v1/admin/review/update/<str:id>/", manager_feedback.update_manager_feedback, name='admin-update-manager-feedback'),
    path("v1/admin/review/answer/<str:answer_id>/", manager_feedback.get_feedback_by_answer, name="admin-manager-feedback-by-answer"),
    path("v1/admin/review/<str:id>/", manager_feedback.get_feedback_by_id, name='admin-manager-review-by-id'),
    # user-review
    path("v1/user/review/answer/<str:answer_id>/", manager_feedback.get_feedback_by_answer, name="user-manager-feedback-by-answer"),
    path("v1/user/review/<str:id>/", manager_feedback.get_feedback_by_id, name='user-manager-review-by-id'),
    # search
    path("v1/search/", search_views.search, name='search'),
    # tag admin
    path("v1/admin/tag/", tag_views.get_all_tags, name='admin-get-all-tags'),
    path("v1/admin/tag/<str:id>/", tag_views.get_tag_by_id, name='admin-get-tag-by-id'),
    # tag user
    path("v1/user/tag/", tag_views.get_all_tags, name='user-get-all-tags'),
    path("v1/user/tag/<str:id>/", tag_views.get_tag_by_id, name='user-get-tag-by-id'),


]
