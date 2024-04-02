import uuid
from app.api.api import SUCCESS
from django.contrib.auth.models import User
from django.conf import settings


def get_char_uuid(length: int = None) -> str:
    id = uuid.uuid4().hex
    return id[:length]


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def is_status_failed(status: int) -> bool:
    return status != SUCCESS


def is_user_admin(user) -> bool:
    return isinstance(user, User)


def generate_filename(filename):
    extension = filename.split('.')[-1]
    new_filename = f"{get_char_uuid(length=20)}.{extension}"
    return new_filename


def upload_path(instance, filename, base_folder):
    filename = generate_filename(filename)
    return f"{base_folder}/{instance.id}/{filename}"


def user_profile_image_path(instance, filename):
    return upload_path(instance=instance, filename=filename, base_folder=settings.S3_USER_FOLDER)


def course_thumbnail_path(instance, filename):
    return upload_path(instance=instance, filename=filename, base_folder=settings.S3_COURSE_FOLDER)


def sub_topic_file_path(instance, filename):
    base_folder = f"{settings.S3_COURSE_FOLDER}/{instance.topic.course.id}/{settings.S3_TOPIC_FOLDER}/{instance.topic.id}/{settings.S3_SUB_TOPIC_FOLDER}"
    return upload_path(instance=instance, filename=filename, base_folder=base_folder)


def assignment_file_path(instance, filename):
    base_folder = f"{settings.S3_COURSE_FOLDER}/{instance.course.id}/{settings.S3_ASSIGNMENT_FOLDER}"
    return upload_path(instance=instance, filename=filename, base_folder=base_folder)


def assignment_submission_file_path(instance, filename):
    base_folder = f"{settings.S3_COURSE_FOLDER}/{instance.user_assignment.user_course_enrollment.course.id}/{settings.S3_ASSIGNMENT_FOLDER}/{instance.user_assignment.assignment.id}/{settings.S3_ASSIGNMENT_SUBMISSIONS_FOLDER}"
    return upload_path(instance=instance, filename=filename, base_folder=base_folder)
