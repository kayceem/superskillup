from app.models import Course


class CourseAccessor:

    @classmethod
    def get_course_by_id(cls, id) -> Course | None:
        return Course.objects.filter(id=id).first()

    @classmethod
    def get_all_courses(cls) -> list[Course] | None:
        return Course.objects.all()
