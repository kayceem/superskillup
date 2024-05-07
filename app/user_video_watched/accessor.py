from app.models import UserVideoWatched
from django.db.models import Count


class UserVideoWatchedAccessor:

    @staticmethod
    def get_watched_videos(enrollment_id):
        return UserVideoWatched.objects.filter(user_course_enrollment=enrollment_id).aggregate(total_watched=Count('id'))['total_watched']

    @staticmethod
    def get_watched_videos_topic(topic_id):
        return UserVideoWatched.objects.filter(sub_topic__topic=topic_id).aggregate(total_watched=Count('id'))['total_watched']

    @staticmethod
    def is_video_watched(enrollment_id, sub_topic_id):
        return UserVideoWatched.objects.filter(user_course_enrollment=enrollment_id, sub_topic=sub_topic_id).exists()
