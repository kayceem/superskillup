from app.utils.utils import get_or_none
from app.models import Topic


class TopicAccessor:

    @classmethod
    def get_topic_by_id(cls, id) -> Topic | None:
        return Topic.objects.filter(id=id).first()

    @classmethod
    def get_topics_by_course(cls, course_id) -> list[Topic] | None:
        return Topic.objects.filter(course_id=course_id).all()
