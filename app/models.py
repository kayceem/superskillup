from django.db import models
from app.utils import get_char_uuid
from app.utils.hashing import hash_raw_password
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, max_length=100, db_index=True, editable=False, default=get_char_uuid)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    FRONTEND = 'frontend'
    BACKEND = 'backend'
    HUMAN_RESOURCE = 'human-resource'
    DEVOPS = 'devops'
    PROJECT_MANAGER = 'project-manager'
    DOMAINS = ((FRONTEND, FRONTEND), (BACKEND, BACKEND), (HUMAN_RESOURCE, HUMAN_RESOURCE), (DEVOPS, DEVOPS), (PROJECT_MANAGER, PROJECT_MANAGER))
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, choices=DOMAINS, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    otp_sent_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

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


class Course(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class Topic(BaseModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class SubTopic(BaseModel):
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sub_topics')
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class Question(BaseModel):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCE = 'advance'
    LEVEL_CHOICES = ((BEGINNER, BEGINNER), (INTERMEDIATE, INTERMEDIATE), (ADVANCE, ADVANCE))
    question = models.CharField(max_length=255)
    helping_text = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='course_questions')
    topic = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='topic_questions')
    sub_topic = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='sub_topic_questions')
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class UserCourseAssignment(BaseModel):
    IN_PROGRESS = 'in-progess'
    COMPLETED = 'completed'
    STATUS = ((IN_PROGRESS, IN_PROGRESS), (COMPLETED, COMPLETED))
    status = models.CharField(max_length=255, choices=STATUS, default=IN_PROGRESS)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-created_at']


class UserAnswer(BaseModel):
    IN_PROGRESS = 'in-progess'
    COMPLETED = 'completed'
    STATUS = ((IN_PROGRESS, IN_PROGRESS), (COMPLETED, COMPLETED))
    user_course_assignment = models.ForeignKey(UserCourseAssignment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    is_reviewed_by_gpt = models.BooleanField(default=False)
    is_reviewed_by_manager = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=STATUS, default=IN_PROGRESS)

    class Meta:
        unique_together = ['user_course_assignment', 'question']


class GptReview(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)


class ManagerFeedback(BaseModel):
    gpt_review = models.ForeignKey(GptReview, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
