from datetime import datetime, timezone
from app.models import Topic


class TopicAccessor:

    @classmethod
    def get_topic_by_id(cls, id) -> Topic | None:
        return Topic.objects.filter(id=id).first()

    @classmethod
    def get_next_topic(cls, topic) -> Topic | None:
        return Topic.objects.filter(created_at__gt=topic.created_at).first()

    @classmethod
    def get_topics_by_course(cls, course_id) -> list[Topic] | None:
        return Topic.objects.filter(course_id=course_id).all()
