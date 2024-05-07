from app.models import SubTopic
from django.db.models import Q


class SubTopicAccessor:

    @classmethod
    def get_sub_topic_by_id(cls, id) -> SubTopic | None:
        return SubTopic.objects.filter(id=id).first()

    @classmethod
    def get_sub_topics_by_topic(cls, topic_id) -> list[SubTopic] | None:
        return SubTopic.objects.filter(topic=topic_id).all()

    @classmethod
    def get_sub_topics_by_course_topic(cls, course_id, topic_id) -> list[SubTopic] | None:
        return SubTopic.objects.filter(topic__course_id=course_id, topic=topic_id).all()

    @classmethod
    def get_total_videos(cls, course_id) -> int | None:
        return SubTopic.objects.filter(topic__course_id=course_id).exclude(video='').count()

    @classmethod
    def get_total_videos_topic(self, topic_id) -> int | None:
        return SubTopic.objects.filter(topic=topic_id).exclude(video='').count()

    @classmethod
    def video_exists(cls, id) -> bool | None:
        return SubTopic.objects.filter(id=id).exclude(video='').exists()
