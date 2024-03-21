from app.models import Course


class CourseAccessor:

    @classmethod
    def get_course_by_id(cls, id) -> Course | None:
        return Course.objects.filter(id=id).first()

    @classmethod
    def get_all_courses(cls) -> list[Course] | None:
        return Course.objects.all()

    @classmethod
    def get_courses_from_ids(cls, course_ids) -> list[Course] | None:
        return Course.objects.filter(id__in=course_ids).all()
