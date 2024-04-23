from app.models import UserCourseEnrollment


class UserCourseEnrollmentAcessor:

    # Only admin
    @staticmethod
    def get_all_enrollments() -> list[UserCourseEnrollment] | None:
        return UserCourseEnrollment.objects.all()

    # Both admin and user
    @staticmethod
    def get_enrollment_by_id(id) -> UserCourseEnrollment | None:
        return UserCourseEnrollment.objects.filter(id=id).first()

    @staticmethod
    def get_user_enrolled_courses(user_id) -> dict | None:
        return UserCourseEnrollment.objects.filter(user_id=user_id).all().values('course')

    @staticmethod
    def get_managers_of_user(user_id) -> dict | None:
        return UserCourseEnrollment.objects.filter(user_id=user_id).all().values('enrolled_by')

    @staticmethod
    def get_users_of_manager(admin_id) -> dict | None:
        return UserCourseEnrollment.objects.filter(enrolled_by__id=admin_id).all().values('user')

    @staticmethod
    def get_user_enrollments(user_id) -> list[UserCourseEnrollment] | None:
        return UserCourseEnrollment.objects.filter(user_id=user_id).all()
