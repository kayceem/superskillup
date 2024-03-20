from app.models import UserProfile


class UserAccessor:

    @classmethod
    def get_user_by_id(cls, id) -> UserProfile | None:
        return UserProfile.objects.filter(id=id).first()

    @classmethod
    def get_user_by_email(cls, email) -> UserProfile | None:
        return UserProfile.objects.filter(email=email).first()
