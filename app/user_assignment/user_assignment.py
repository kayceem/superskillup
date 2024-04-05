from app.user_assignment.accessor import UserAssignmentAcessor


class UserAssignment:

    @staticmethod
    def get_user_assignment_by_id(id):
        return UserAssignmentAcessor.get_user_assignment_by_id(id)

    @staticmethod
    def get_all_user_assignments_by_user(user_id):
        return UserAssignmentAcessor.get_all_user_assignments_by_user(user_id)

    @staticmethod
    def get_all_user_assignments_by_course(course_id):
        return UserAssignmentAcessor.get_all_user_assignments_by_course(course_id)

    @staticmethod
    def get_user_assignments_by_course(user_id, course_id):
        return UserAssignmentAcessor.get_user_assignments_by_course(user_id, course_id)

    @staticmethod
    def get_user_assignments_by_enrollment(enrollment_id):
        return UserAssignmentAcessor.get_user_assignments_by_enrollment(enrollment_id)

    @staticmethod
    def get_assignment_user(user_assignment):
        if not user_assignment:
            return None
        return user_assignment.user_course_enrollment.user

    @staticmethod
    def delete_user_assignment(user_assignment):
        if not user_assignment:
            return None
        return user_assignment.delete()
