from typing import Any
from django.contrib import admin
from django.http import HttpResponseRedirect
from app.models import UserProfile, QuestionAnswer, Assignment, UserAssignment, UserAssignmentSubmission, UserCourseEnrollment, Question, Course, Topic, SubTopic, GptReview, ManagerFeedback, Tag, UserVideoWatched
from django.contrib import messages
from django.contrib.auth.models import User

from app.services import email_service


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

    change_form_template = 'admin/soft_delete.html'

    def response_change(self, request, obj):
        if obj is None:
            return super().response_change(request, obj)

        if "_soft-delete" in request.POST:
            if obj.is_deleted:
                self.message_user(request, "Already deleted", level=messages.ERROR)
                return HttpResponseRedirect(".")
            obj.delete()
            self.message_user(request, "Soft delete successfull.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def delete_model(self, request, obj):
        obj.hard_delete()

    def get_queryset(self, request):
        return self.model.all_objects.get_queryset()

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return []
        if not obj.is_deleted:
            return ['id', 'is_deleted']
        fields = ([f.name for f in self.model._meta.fields])
        return fields

    def get_inlines(self, request, obj):
        if not obj:
            return []
        if not obj.is_deleted:
            return self.inlines
        return []

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_soft_delete'] = True
        return super(BaseAdminModel, self).change_view(request, object_id, extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj is None:
            return super().render_change_form(request, context, add, change, form_url, obj)
        if obj.is_deleted:
            context.update({
                'show_save': False,
                'show_save_and_continue': False,
                'show_save_and_add_another': False,
                'show_soft_delete': False,
            })
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdminModel):
    list_display = ('name', 'email', 'is_verified', 'is_deleted')


@admin.register(Tag)
class TagAdmin(BaseAdminModel):
    list_display = ('name', 'is_deleted')


@admin.register(Course)
class CourseAdmin(BaseAdminModel):
    list_display = ('name', 'category', 'get_tags', 'created_by', 'is_deleted')
    inlines = [TopicInline, AssignmentInline]
    search_fields = ['name', 'created_by']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            qs = User.objects.get_queryset()
            if not request.user.is_superuser:
                qs = qs.filter(id=request.user.id)
            kwargs["queryset"] = qs
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_topics(self, obj):
        return "\n".join([topic.name for topic in obj.topics.all()])

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if fields == []:
            return fields
        if obj.is_deleted:
            return fields
        if not request.user.is_superuser:
            fields.append('created_by')
        fields.append('get_topics')
        return fields

    get_topics.short_description = "Topics"
    get_tags.short_description = "Tags"


@admin.register(Topic)
class TopicAdmin(BaseAdminModel):
    list_display = ('name', 'course', 'is_deleted')
    inlines = [SubTopicInline]
    search_fields = ['name']

    def get_sub_topics(self, obj):
        return "\n".join([topic.name for topic in obj.sub_topics.all()])

    get_sub_topics.short_description = "Sub Topics"

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if fields == []:
            return fields
        if obj.is_deleted:
            return fields
        fields.append('get_sub_topics')
        return fields


@admin.register(SubTopic)
class SubTopicAdmin(BaseAdminModel):
    list_display = ('name', "topic", 'get_course', 'is_deleted')
    search_fields = ['name']
    inlines = [QuestionInline]

    def get_course(self, obj):
        return obj.topic.course

    get_course.short_description = "Course"


@admin.register(Question)
class QuestionAdmin(BaseAdminModel):
    list_display = ('question', 'course', 'topic', 'sub_topic', 'is_deleted')
    search_fields = ['question']

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if fields == []:
            return fields
        if obj.is_deleted:
            return fields
        fields.extend(['course', 'topic'])
        return fields


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(BaseAdminModel):
    list_display = ('user_course_enrollment', 'question', 'answer', 'is_deleted')
    search_fields = ['question']

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if fields == []:
            return fields
        fields = ([f.name for f in self.model._meta.fields])
        fields.extend(['gpt_review_remarks', 'gpt_review_score'])
        return fields

    def gpt_review_remarks(self, obj):
        return obj.gptreview.remarks if obj.is_reviewed_by_gpt else "No GPT Review"

    def gpt_review_score(self, obj):
        return obj.gptreview.score if obj.is_reviewed_by_gpt else "No GPT Review"


@admin.register(Assignment)
class AssignmentAdmin(BaseAdminModel):
    list_display = ('title', 'course', 'created_by', 'is_deleted')


@admin.register(UserCourseEnrollment)
class UserCourseEnrollmentAdmin(BaseAdminModel):
    list_display = ('user', 'course', 'status', 'enrolled_by', 'is_deleted')
    exclude = ('next_topic_created_at', 'next_topic_start_time')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "enrolled_by":
            qs = User.objects.get_queryset()
            if not request.user.is_superuser:
                qs = qs.filter(id=request.user.id)
            kwargs["queryset"] = qs
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(UserAssignment)
class UserAssignmentAdmin(BaseAdminModel):
    list_display = ('assignment', 'user_course_enrollment', 'deadline', 'is_submitted', 'is_deleted')

    def is_submitted(self, obj) -> bool:
        return UserAssignmentSubmission.objects.filter(user_assignment=obj).exists()

    is_submitted.short_description = "Submitted"
    is_submitted.boolean = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        breakpoint()
        email_service.send_assignment_assigned_mail(obj)


@admin.register(UserAssignmentSubmission)
class UserAssignmentSubmissionAdmin(BaseAdminModel):
    list_display = ('user_assignment', 'submitted_at', 'is_deleted')

    def submitted_at(self, obj):
        return obj.created_at

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if fields == []:
            return fields
        fields = ([f.name for f in self.model._meta.fields])
        return fields

    submitted_at.short_description = "Submitted at"


@admin.register(GptReview)
class GptReviewAdmin(BaseAdminModel):
    list_display = ('question_answer', 'remarks', 'score', 'is_deleted')


@admin.register(ManagerFeedback)
class ManagerFeedbackAdmin(BaseAdminModel):
    list_display = ('gpt_review', 'remarks', 'score', 'is_deleted')

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if fields == []:
            return fields
        if obj.is_deleted:
            return fields
        fields.extend(['gpt_review_remarks', 'gpt_review_score'])
        return fields

    def gpt_review_remarks(self, obj):
        return obj.gpt_review.remarks if obj.gpt_review else "No GPT Review"

    def gpt_review_score(self, obj):
        return obj.gpt_review.score if obj.gpt_review else "No GPT Review"
    gpt_review_remarks.short_description = 'GPT Review'
    gpt_review_score.short_description = 'GPT Review Score'


@admin.register(UserVideoWatched)
class UserVideoWatchedAdmin(BaseAdminModel):
    list_display = ('user_course_enrollment', 'sub_topic')
