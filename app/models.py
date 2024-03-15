from django.db import models
from app.utils import get_char_uuid
from app.utils.hashing import hash_raw_password


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
    otp = models.CharField(max_length = 10, null = True, blank = True)
    otp_sent_date = models.DateTimeField(null = True, blank = True)
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
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Topic(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to='documents/topic/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)


class SubTopic(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to='documents/sub_topic/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)


class Question(BaseModel):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCE = 'advance'
    LEVEL_CHOICES = ((BEGINNER, BEGINNER), (INTERMEDIATE, INTERMEDIATE), (ADVANCE, ADVANCE))
    question = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    helping_text = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, null=True, blank=True)


class UserAssignment(BaseModel):
    IN_PROGRESS = 'in-progess'
    COMPLETED = 'completed'
    STATUS = ((IN_PROGRESS, IN_PROGRESS), (COMPLETED, COMPLETED))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS, default=IN_PROGRESS)

    class Meta:
        unique_together = ['user', 'question']


class UserAnswer(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    is_reviewed_by_gpt = models.BooleanField(default=False)
    is_reviewed_by_manager = models.BooleanField(default=False)


class GptReview(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)


class ManageFeedback(BaseModel):
    gpt_review = models.ForeignKey(GptReview, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
