# Generated by Django 5.0.3 on 2024-04-23 09:54

import app.utils.utils
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GptReview',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('score', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubTopic',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('video', models.FileField(blank=True, max_length=255, null=True, upload_to=app.utils.utils.sub_topic_file_path, validators=[django.core.validators.FileExtensionValidator(['mp4', 'webm', 'mov'])])),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to=app.utils.utils.sub_topic_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'docx', 'txt'])])),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
                ('otp_sent_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=app.utils.utils.user_profile_image_path)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.CharField(blank=True, choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advance', 'advance')], max_length=255, null=True)),
                ('thumbnail', models.ImageField(blank=True, max_length=255, null=True, upload_to=app.utils.utils.course_thumbnail_path)),
                ('category', models.CharField(blank=True, choices=[('Web Development', 'Web Development'), ('Frontend Development', 'Frontend Development'), ('Backend Development', 'Backend Development'), ('Full Stack Development', 'Full Stack Development'), ('Web Design & User Experience', 'Web Design & User Experience'), ('Management', 'Management'), ('Marketing', 'Marketing'), ('Management', 'Management')], max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='app.tag')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to=app.utils.utils.assignment_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'docx', 'txt'])])),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='app.course')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManagerFeedback',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('score', models.PositiveIntegerField(blank=True, null=True)),
                ('gpt_review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.gptreview')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('question', models.CharField(max_length=255)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_questions', to='app.course')),
                ('sub_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_topic_questions', to='app.subtopic')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('answer', models.TextField(blank=True, null=True)),
                ('is_reviewed_by_gpt', models.BooleanField(default=False)),
                ('is_reviewed_by_manager', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
            ],
        ),
        migrations.AddField(
            model_name='gptreview',
            name='question_answer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.questionanswer'),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='app.course')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='subtopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_topics', to='app.topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_questions', to='app.topic'),
        ),
        migrations.CreateModel(
            name='UserAssignment',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='app.assignment')),
            ],
        ),
        migrations.CreateModel(
            name='UserAssignmentSubmission',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, null=True)),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to=app.utils.utils.assignment_submission_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'docx', 'txt'])])),
                ('description', models.TextField(blank=True, null=True)),
                ('user_assignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='app.userassignment')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCourseEnrollment',
            fields=[
                ('id', models.CharField(db_index=True, default=app.utils.utils.get_char_uuid, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('in-progess', 'in-progess'), ('completed', 'completed')], default='in-progess', max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
                ('enrolled_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='app.userprofile')),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
        migrations.AddField(
            model_name='userassignment',
            name='user_course_enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='app.usercourseenrollment'),
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='user_course_enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usercourseenrollment'),
        ),
        migrations.AlterUniqueTogether(
            name='userassignment',
            unique_together={('user_course_enrollment', 'assignment')},
        ),
        migrations.AlterUniqueTogether(
            name='questionanswer',
            unique_together={('user_course_enrollment', 'question')},
        ),
    ]
