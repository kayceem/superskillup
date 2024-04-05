from django.contrib import admin
from app.models import UserProfile, QuestionAnswer, Assignment, UserAssignment, UserAssignmentSubmission, UserCourseEnrollment, Question, Course, Topic, SubTopic, GptReview, ManagerFeedback, Tag


class SubTopicInline(admin.TabularInline):
    model = SubTopic
    show_change_link = True
    extra = 0


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    show_change_link = True


class BaseAdminModel(admin.ModelAdmin):

    def delete_model(self, request, obj):
        obj.hard_delete()

    def get_queryset(self, request):
        return self.model.all_objects.all()


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdminModel):
    list_display = ('id', 'name', 'email', "is_verified", "is_active")


@admin.register(Tag)
class TagAdmin(BaseAdminModel):
    list_display = ('id', 'name')


@admin.register(Course)
class CourseAdmin(BaseAdminModel):
    list_display = ('name', 'get_topics')
    inlines = [TopicInline]
    search_fields = ['name']

    def get_topics(self, obj):
        return ", ".join([topic.name for topic in obj.topics.all()])

    get_topics.short_description = "Topics"


@admin.register(Topic)
class TopicAdmin(BaseAdminModel):
    list_display = ('name', "course", "get_sub_topics")
    inlines = [SubTopicInline]
    search_fields = ['name']
    fieldsets = ((None, {'fields': ('name', 'course')}),)

    def get_sub_topics(self, obj):
        return ", ".join([topic.name for topic in obj.sub_topics.all()])

    get_sub_topics.short_description = "Sub Topics"


@admin.register(SubTopic)
class SubTopicAdmin(BaseAdminModel):
    list_display = ('name', "topic", "get_course")
    search_fields = ['name']

    def get_course(self, obj):
        return obj.topic.course

    get_course.short_description = "Course"


@admin.register(Question)
class QuestionAdmin(BaseAdminModel):
    list_display = ('id', 'question', 'course', 'topic', 'sub_topic')
    search_fields = ['question']


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(BaseAdminModel):
    list_display = ('id', 'user_course_enrollment', 'question', 'answer')
    search_fields = ['question']


@admin.register(Assignment)
class AssignmentAdmin(BaseAdminModel):
    list_display = ('id', 'title', 'course', 'created_by')


@admin.register(UserCourseEnrollment)
class UserCourseEnrollmentAdmin(BaseAdminModel):
    list_display = ('id', 'user', 'course', 'status')


@admin.register(UserAssignment)
class UserAssignmentAdmin(BaseAdminModel):
    list_display = ('id', 'assignment', 'user_course_enrollment')


@admin.register(UserAssignmentSubmission)
class UserAssignmentSubmissionAdmin(BaseAdminModel):
    list_display = ('id', 'user_assignment')


@admin.register(GptReview)
class GptReviewAdmin(BaseAdminModel):
    list_display = ('id', 'question_answer', 'remarks', 'score')


@admin.register(ManagerFeedback)
class ManagerFeedbackAdmin(BaseAdminModel):
    list_display = ('id', 'gpt_review', 'remarks', 'score')
