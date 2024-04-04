from app.models import UserProfile


class UserAccessor:

    @classmethod
    def get_user_by_id(cls, id) -> UserProfile | None:
        return UserProfile.objects.filter(id=id).first()

    @classmethod
    def get_user_by_email(cls, email) -> UserProfile | None:
        return UserProfile.objects.filter(email=email).first()

    @classmethod
    def get_all_users(cls) -> list[UserProfile] | None:
        return UserProfile.objects.filter(is_verified=True).all()

    @classmethod
    def get_users_from_ids(cls, user_ids) -> list[UserProfile] | None:
        return UserProfile.objects.filter(id__in=user_ids).all()
