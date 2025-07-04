from app.user_video_watched.accessor import UserVideoWatchedAccessor


class UserVideo:
    @staticmethod
    def get_watched_videos(enrollment_id):
        return UserVideoWatchedAccessor.get_watched_videos(enrollment_id)

    @staticmethod
    def get_watched_videos_topic(topic_id):
        return UserVideoWatchedAccessor.get_watched_videos_topic(topic_id)

    @staticmethod
    def is_video_watched(enrollment_id, sub_topic_id):
        return UserVideoWatchedAccessor.is_video_watched(enrollment_id, sub_topic_id)
