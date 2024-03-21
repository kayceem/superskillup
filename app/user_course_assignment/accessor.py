from app.models import UserCourseAssignment


class UserCourseAssignmentAcessor:

    # Only admin
    @staticmethod
    def get_all_assignments() -> UserCourseAssignment | None:
        return UserCourseAssignment.objects.all()

    # Both admin and user
    @staticmethod
    def get_assignment_by_id(id) -> UserCourseAssignment | None:
        return UserCourseAssignment.objects.filter(id=id).first()

    @staticmethod
    def get_user_assigned_courses(user_id) -> UserCourseAssignment | None:
        return UserCourseAssignment.objects.filter(user_id=user_id).all().values('course')

    # @staticmethod
    # def get_user_assigned_topics(id) -> UserCourseAssignment | None:
    #     return UserCourseAssignment.objects.filter(id=id).first().course.topics.all()

    # @staticmethod
    # def get_user_assigned_sub_topics(user_id, topic_id) -> UserCourseAssignment | None:
    #     return UserCourseAssignment.objects.filter(user_id=user_id, topic_id=topic_id).first().course..all()

    # @staticmethod
    # def get_user_assigned_questions(user) -> UserCourseAssignment | None:
    #     return UserCourseAssignment.objects.filter(user_id=user).all().values('question')
