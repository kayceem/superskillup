from app.user_assignment_submission.accessor import UserAssignmentSubmissionAccessor


class UserAssignmentSubmission:

    @staticmethod
    def get_user_assignment_submission_by_id(id):
        return UserAssignmentSubmissionAccessor.get_user_assignment_submission_by_id(id)

    @staticmethod
    def get_user_assignment_submission_by_user_assignment(user_assignment_id):
        return UserAssignmentSubmissionAccessor.get_user_assignment_submission_by_user_assignment(user_assignment_id)

    @staticmethod
    def get_user_assignment_submission_user(assignment_submission):
        if not assignment_submission:
            return None
        return assignment_submission.user_assignment.user_course_enrollment.user
