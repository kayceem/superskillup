from django.contrib import admin
from app.models import UserProfile, QuestionAnswer, Assignment, UserAssignment, UserAssignmentSubmission, UserCourseEnrollment, Question, Course, Topic, SubTopic, GptReview, ManagerFeedback, Tag
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# admin.site.unregister(User)
# admin.site.unregister(Group)


class SubTopicInline(admin.TabularInline):
    model = SubTopic
    show_change_link = True
    extra = 0


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    show_change_link = True


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', "is_verified", "is_active")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_topics')
    inlines = [TopicInline]
    search_fields = ['name']

    def get_topics(self, obj):
        return ", ".join([topic.name for topic in obj.topics.all()])

    get_topics.short_description = "Topics"

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted', 'url')
    #     return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    # def changeform_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted', 'url')
    #     return super().changeform_view(request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', "course", "get_sub_topics")
    inlines = [SubTopicInline]
    search_fields = ['name']
    fieldsets = ((None, {'fields': ('name', 'course')}),)

    def get_sub_topics(self, obj):
        return ", ".join([topic.name for topic in obj.sub_topics.all()])

    get_sub_topics.short_description = "Sub Topics"

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted',)
    #     return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    # def changeform_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted',)
    #     return super().changeform_view(request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('name', "topic", "get_course")
    search_fields = ['name']

    def get_course(self, obj):
        return obj.topic.course

    get_course.short_description = "Course"

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted',)
    #     return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    # def changeform_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted',)
    #     return super().changeform_view(request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'course', 'topic', 'sub_topic')
    search_fields = ['question']

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted',)
    #     return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    # def changeform_view(self, request, object_id, form_url='', extra_context=None):
    #     self.exclude = ('is_deleted',)
    #     return super().changeform_view(request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'created_by')


@admin.register(UserCourseEnrollment)
class UserCourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'status')


@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'user_course_enrollment')


@admin.register(UserAssignmentSubmission)
class UserAssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_assignment')


@admin.register(GptReview)
class GptReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_answer', 'remarks', 'score')


@admin.register(ManagerFeedback)
class ManagerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'gpt_review', 'remarks', 'score')
