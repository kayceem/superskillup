from app.models import UserAssignmentSubmission


class UserAssignmentSubmissionAccessor:

    @staticmethod
    def get_user_assignment_submission_by_id(id):
        return UserAssignmentSubmission.objects.filter(id=id).first()

    @staticmethod
    def get_user_assignment_submission_by_user_assignment(user_assignment_id):
        return UserAssignmentSubmission.objects.filter(user_assignment=user_assignment_id).first()
