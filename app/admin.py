# from django.contrib import admin

# from app.models import UserProfile, UserAnswer, UserCourseAssignment, Question, Course, Topic, SubTopic, GptReview, ManagerFeedback


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', "is_verified", "is_active")


# @admin.register(UserAnswer)
# class UserAnswerAdmin(admin.ModelAdmin):
#     list_display = ('id', "user_course_assignment", "question", "answer", "is_reviewed_by_gpt", "is_reviewed_by_manager")


# @admin.register(UserCourseAssignment)
# class UserAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('id', "user", "course", "deadline", "status")


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('id', "question", "level", "course", "topic", "sub_topic")


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')


# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', "course")


# @admin.register(SubTopic)
# class SubTopicAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', "topic")


# @admin.register(GptReview)
# class GptReviewAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', "question", "remarks", "score")


# @admin.register(ManagerFeedback)
# class ManagerFeedbackAdmin(admin.ModelAdmin):
#     list_display = ('id', 'gpt_review', "remarks", "score")
