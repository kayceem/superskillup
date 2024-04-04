from app.models import SubTopic


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
