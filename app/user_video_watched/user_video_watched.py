from app.user_video_watched.accessor import UserVideoWatchedAccessor


class UserVideo:
    @staticmethod
    def get_watched_videos(enrollment_id):
        return UserVideoWatchedAccessor.get_watched_videos(enrollment_id)
