from django.contrib import admin
from app.models import UserProfile, QuestionAnswer, Assignment, UserAssignment, UserAssignmentSubmission, UserCourseEnrollment, Question, Course, Topic, SubTopic, GptReview, ManagerFeedback, Tag


class AssignmentInline(admin.TabularInline):
    model = Assignment
    show_change_link = True
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True
    extra = 0


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

    def get_readonly_fields(self, request, obj=None):
        return ['id'] if obj else []


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdminModel):
    list_display = ('name', 'email', "is_verified", "is_active")


@admin.register(Tag)
class TagAdmin(BaseAdminModel):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(BaseAdminModel):
    list_display = ('name', 'category', 'get_tags', 'created_by')
    inlines = [TopicInline, AssignmentInline]
    search_fields = ['name']

    def get_topics(self, obj):
        return "\n".join([topic.name for topic in obj.topics.all()])

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def get_readonly_fields(self, request, obj=None):
        return ['id', 'get_topics'] if obj else []

    get_topics.short_description = "Topics"
    get_tags.short_description = "Tags"


@admin.register(Topic)
class TopicAdmin(BaseAdminModel):
    list_display = ('name', 'course',)
    inlines = [SubTopicInline]
    search_fields = ['name']

    def get_sub_topics(self, obj):
        return "\n".join([topic.name for topic in obj.sub_topics.all()])

    get_sub_topics.short_description = "Sub Topics"

    def get_readonly_fields(self, request, obj=None):
        return ['id', 'get_sub_topics'] if obj else []


@admin.register(SubTopic)
class SubTopicAdmin(BaseAdminModel):
    list_display = ('name', "topic", "get_course")
    search_fields = ['name']
    inlines = [QuestionInline]

    def get_course(self, obj):
        return obj.topic.course

    get_course.short_description = "Course"


@admin.register(Question)
class QuestionAdmin(BaseAdminModel):
    list_display = ('question', 'course', 'topic', 'sub_topic')
    search_fields = ['question']

    def get_readonly_fields(self, request, obj=None):
        return ['id', 'course', 'topic'] if obj else []


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(BaseAdminModel):
    list_display = ('user_course_enrollment', 'question', 'answer')
    search_fields = ['question']


@admin.register(Assignment)
class AssignmentAdmin(BaseAdminModel):
    list_display = ('title', 'course', 'created_by')


@admin.register(UserCourseEnrollment)
class UserCourseEnrollmentAdmin(BaseAdminModel):
    list_display = ('user', 'course', 'status', 'enrolled_by')


@admin.register(UserAssignment)
class UserAssignmentAdmin(BaseAdminModel):
    list_display = ('assignment', 'user_course_enrollment', 'deadline', 'is_submitted')

    def is_submitted(self, obj) -> bool:
        return UserAssignmentSubmission.objects.filter(user_assignment=obj).exists()

    is_submitted.short_description = "Submitted"
    is_submitted.boolean = True


@admin.register(UserAssignmentSubmission)
class UserAssignmentSubmissionAdmin(BaseAdminModel):
    list_display = ('user_assignment', 'submitted_at')

    def submitted_at(self, obj):
        return obj.created_at

    submitted_at.short_description = "Submitted at"


@admin.register(GptReview)
class GptReviewAdmin(BaseAdminModel):
    list_display = ('question_answer', 'remarks', 'score')


@admin.register(ManagerFeedback)
class ManagerFeedbackAdmin(BaseAdminModel):
    list_display = ('gpt_review', 'remarks', 'score')

    def get_readonly_fields(self, request, obj=None):
        return ['id', 'gpt_review_remarks', 'gpt_review_score'] if obj else []

    def gpt_review_remarks(self, obj):
        return obj.gpt_review.remarks if obj.gpt_review else "No GPT Review"

    def gpt_review_score(self, obj):
        return obj.gpt_review.score if obj.gpt_review else "No GPT Review"
    gpt_review_remarks.short_description = 'GPT Review'
    gpt_review_score.short_description = 'GPT Review Score'
