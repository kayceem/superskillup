from app.models import UserVideoWatched


class UserVideoWatchedAccessor:

    @staticmethod
    def get_watched_videos(enrollment_id):
        return UserVideoWatched.objects.filter(user_course_enrollment=enrollment_id).count()
