from app.utils.utils import get_or_none
from app.models import Course


class CourseAccessor:

    @classmethod
    def get_course(cls, **kwargs) -> Course | None:
        return get_or_none(Course, **kwargs)

    @classmethod
    def filter_course(cls, filters: dict) -> list[Course] | None:
        return Course.objects.filter(**filters)
