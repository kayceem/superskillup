from app.sub_topic.accessor import SubTopicAccessor
import os
from moviepy.editor import VideoFileClip


class SubTopic:

    def __init__(self, sub_topic):
        self.sub_topic = sub_topic

    @staticmethod
    def get_sub_topic_by_id(sub_topic_id):
        return SubTopicAccessor.get_sub_topic_by_id(id=sub_topic_id)

    @staticmethod
    def get_total_videos(course_id):
        return SubTopicAccessor.get_total_videos(course_id)

    @staticmethod
    def get_total_videos_topic(topic_id):
        return SubTopicAccessor.get_total_videos_topic(topic_id)

    @staticmethod
    def video_exists(id):
        return SubTopicAccessor.video_exists(id)

    @staticmethod
    def get_sub_topics_by_topic(topic_id):
        return SubTopicAccessor.get_sub_topics_by_topic(topic_id=topic_id)

    @staticmethod
    def get_sub_topics_by_course_topic(course_id, topic_id):
        return SubTopicAccessor.get_sub_topics_by_course_topic(course_id=course_id, topic_id=topic_id)

    @staticmethod
    def delete_sub_topic(sub_topic):
        return sub_topic.delete()

    @staticmethod
    def get_video_length(video):
        try:
            video_path = video.temporary_file_path()
            if os.path.exists(video_path):
                clip = VideoFileClip(video_path)
                return int(clip.duration)
        except:
            return None
