from datetime import datetime, timezone
from app.utils.utils import user_profile_image_path, course_thumbnail_path, sub_topic_file_path, assignment_file_path, assignment_submission_file_path
from django.db import models
from django.forms import ValidationError
from app.utils import get_char_uuid
from app.utils.hashing import hash_raw_password
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import transaction
from app.utils import validators


class CustomQuerySet(models.QuerySet):
    def delete(self):
        for obj in self.all():
            obj.delete()
        return


class CustomObjectManager(models.Manager):

    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db).filter(is_deleted=False)
        # return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, max_length=100, db_index=True, editable=False, default=get_char_uuid)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = CustomObjectManager()
    all_objects = models.Manager()

    def delete(self):
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        with transaction.atomic():
            for field in self._meta.get_fields():

                if isinstance(field, GenericRelation):
                    print(field.related_model)
                    continue

                RelatedModel = field.related_model
                if not RelatedModel:
                    continue

                if field.one_to_one:
                    related_object = getattr(self, field.name, None)
                    # print("one to one field ", RelatedModel, " ", related_object)
                    if related_object:
                        self.__delete_related_object(field, related_object)

                elif field.one_to_many:
                    related_objects = getattr(self, field.get_accessor_name()).all()
                    for related_object in related_objects:
                        if related_object:
                            # print("one to many field ", RelatedModel, " ", related_object)
                            self.__delete_related_object(field, related_object)
                else:
                    # print("many to many field ", field, " ",)
                    continue

            self.is_deleted = True
            self.save(update_fields=['is_deleted'])
            return True

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __delete_related_object(self, field, related_object):
        if hasattr(field, 'on_delete'):
            on_delete = field.on_delete
        else:
            return

        if on_delete is models.CASCADE:
            related_object.delete()
        else:
            return

    class Meta:
        abstract = True
        ordering = ['created_at']


class UserProfile(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    otp = models.CharField(max_length=10, null=True, blank=True)
    otp_sent_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        user = UserProfile.objects.filter(pk=self.pk).first()
        if not user:
            self.password = hash_raw_password(self.password)
            return super().save(*args, **kwargs)
        password_changed = self.password != user.password
        if not password_changed:
            return super().save(*args, **kwargs)
        self.password = hash_raw_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(BaseModel):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCE = 'advance'

    LEVEL_CHOICES = (
        (BEGINNER, BEGINNER),
        (INTERMEDIATE, INTERMEDIATE),
        (ADVANCE, ADVANCE),
    )

    WEB_DEV = 'Web Development'
    FRONTEND = 'Frontend Development'
    BACKEND = 'Backend Development'
    FULL_STACK = 'Full Stack Development'
    WEB_DESING = 'Web Design & User Experience'
    MANAGEMENT = 'Management'
    MARKETING = 'Marketing'
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    MACHINE_LEARNING = "Machine Learning"
    TESTTING_AUTOMATION = "Testing & Automation"
    OTHERS = "Others"

    CATEGORY_CHOICES = (
        (WEB_DEV, WEB_DEV),
        (FRONTEND, FRONTEND),
        (BACKEND, BACKEND),
        (FULL_STACK, FULL_STACK),
        (WEB_DESING, WEB_DESING),
        (MANAGEMENT, MANAGEMENT),
        (MARKETING, MARKETING),
        (ARTIFICIAL_INTELLIGENCE, ARTIFICIAL_INTELLIGENCE),
        (MACHINE_LEARNING, MACHINE_LEARNING),
        (TESTTING_AUTOMATION, TESTTING_AUTOMATION),
        (OTHERS, OTHERS),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=course_thumbnail_path, max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.name}'


class Topic(BaseModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class SubTopic(BaseModel):
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sub_topics')
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to=sub_topic_file_path, max_length=255, blank=True, null=True, validators=[validators.get_video_extension_validator()])
    video_length = models.IntegerField(blank=True, null=True)
    file = models.FileField(upload_to=sub_topic_file_path, max_length=255, blank=True, null=True, validators=[validators.get_document_extension_validator()])

    def clean(self):
        filled_fields = sum(1 for field in ['url', 'video', 'file'] if getattr(self, field))
        if filled_fields > 1:
            raise ValidationError("Only one of 'url', 'video', or 'file' should be filled.")
        super().clean()

    def __str__(self):
        return f'{self.name}'


class UserCourseEnrollment(BaseModel):
    IN_PROGRESS = 'in-progess'
    COMPLETED = 'completed'
    STATUS = ((IN_PROGRESS, IN_PROGRESS), (COMPLETED, COMPLETED))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS, default=IN_PROGRESS)
    enrolled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    next_topic_created_at = models.DateTimeField(null=True, blank=True)
    next_topic_start_time = models.DateTimeField(null=True, blank=True)
    interval_days = models.PositiveIntegerField(null=True, blank=True, default=1)

    def clean(self):
        course = getattr(self, "course", None)
        if not course:
            return
        if self.course.topics.count() == 0:
            raise ValidationError("Course must have at least one topic to enroll users.")
        super().clean()

    def save(self, *args, **kwargs):
        if not self.next_topic_created_at:
            self.next_topic_created_at = self.course.topics.first().created_at
            self.next_topic_start_time = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}-{self.course}'

    class Meta:
        unique_together = ['user', 'course']


class Assignment(BaseModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=assignment_file_path, max_length=255, blank=True, null=True, validators=[validators.get_document_extension_validator()])

    def __str__(self):
        return f'{self.course}-{self.title}'


class UserAssignment(BaseModel):
    user_course_enrollment = models.ForeignKey(UserCourseEnrollment, on_delete=models.CASCADE, related_name='assignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='users', null=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def clean(self):
        user_course_enrollment = getattr(self, "user_course_enrollment", None)
        assignment = getattr(self, "assignment", None)
        if not user_course_enrollment or not assignment:
            return
        if self.user_course_enrollment.course != self.assignment.course:
            raise ValidationError("Assignment course must match with user's enrolled course.")

    def __str__(self):
        return f'{self.user_course_enrollment}-{self.assignment}'

    class Meta:
        unique_together = ['user_course_enrollment', 'assignment']


class UserAssignmentSubmission(BaseModel):
    user_assignment = models.OneToOneField(UserAssignment, on_delete=models.CASCADE, related_name='submissions')
    url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to=assignment_submission_file_path, max_length=255, blank=True, null=True, validators=[validators.get_document_extension_validator()])
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_assignment}'


class Question(BaseModel):
    question = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_questions', null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_questions', null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='sub_topic_questions')

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        sub_topic = SubTopic.objects.filter(pk=self.sub_topic.pk).first()
        self.topic = sub_topic.topic
        self.course = sub_topic.topic.course
        return super().save(*args, **kwargs)


class QuestionAnswer(BaseModel):
    user_course_enrollment = models.ForeignKey(UserCourseEnrollment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    is_reviewed_by_gpt = models.BooleanField(default=False)
    is_reviewed_by_manager = models.BooleanField(default=False)

    def clean(self):
        if self.user_course_enrollment.course != self.question.course:
            raise ValidationError("Question course must match with user's enrolled course.")

    def __str__(self):
        return f'{self.user_course_enrollment}-{self.question}'

    class Meta:
        unique_together = ['user_course_enrollment', 'question']


class GptReview(BaseModel):
    question_answer = models.OneToOneField(QuestionAnswer, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.question_answer}'


class ManagerFeedback(BaseModel):
    gpt_review = models.OneToOneField(GptReview, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.gpt_review}'


class UserVideoWatched(BaseModel):
    user_course_enrollment = models.ForeignKey(UserCourseEnrollment, on_delete=models.CASCADE, related_name='videos_watched')
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='videos_watched')

    class Meta:
        unique_together = ['user_course_enrollment', 'sub_topic']
