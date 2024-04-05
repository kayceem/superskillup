from app.models import UserAssignment


class UserAssignmentAcessor:

    @staticmethod
    def get_user_assignment_by_id(id) -> UserAssignment | None:
        return UserAssignment.objects.filter(id=id).first()

    @staticmethod
    def get_all_user_assignments_by_user(user_id) -> list[UserAssignment] | None:
        return UserAssignment.objects.filter(user_course_enrollment__user=user_id).all()

    @staticmethod
    def get_all_user_assignments_by_course(course_id) -> list[UserAssignment] | None:
        return UserAssignment.objects.filter(user_course_enrollment__course=course_id).all()

    @staticmethod
    def get_user_assignments_by_course(user_id, course_id) -> list[UserAssignment] | None:
        return UserAssignment.objects.filter(user_course_enrollment__user=user_id, user_course_enrollment__course=course_id).all()

    @staticmethod
    def get_user_assignments_by_enrollment(enrollment_id) -> list[UserAssignment] | None:
        return UserAssignment.objects.filter(user_course_enrollment=enrollment_id).all()
