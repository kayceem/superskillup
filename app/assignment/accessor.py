from app.models import Assignment


class AssignmentAccessor:

    @classmethod
    def get_assignment_by_id(cls, id) -> Assignment | None:
        return Assignment.objects.filter(id=id).first()

    @classmethod
    def get_assignments_by_course(cls, course_id) -> list[Assignment] | None:
        return Assignment.objects.filter(course=course_id).all()
