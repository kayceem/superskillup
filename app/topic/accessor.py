from app.utils.utils import get_or_none
from app.models import Topic


class TopicAccessor:

    @classmethod
    def get_topic(cls, **kwargs) -> Topic | None:
        return get_or_none(Topic, **kwargs)

    @classmethod
    def filter_topic(cls, filters: dict) -> list[Topic] | None:
        return Topic.objects.filter(**filters)
