from app.models import UserVideoWatched


class UserVideoWatchedAccessor:

    @staticmethod
    def get_watched_videos(enrollment_id):
        return UserVideoWatched.objects.filter(user_course_enrollment=enrollment_id).count()

    @staticmethod
    def get_watched_videos_topic(topic_id):
        return UserVideoWatched.objects.filter(sub_topic__topic=topic_id).count()

    @staticmethod
    def is_video_watched(enrollment_id, sub_topic_id):
        return UserVideoWatched.objects.filter(user_course_enrollment=enrollment_id, sub_topic=sub_topic_id).exists()
