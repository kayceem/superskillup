from app.utils.utils import get_or_none
from app.models import UserProfile


class UserAccessor:

    @classmethod
    def get_user(cls, **kwargs) -> UserProfile | None:
        return get_or_none(UserProfile, **kwargs)

    @classmethod
    def filter_user(cls, filters: dict) -> list[UserProfile]:
        return UserProfile.objects.filter(**filters)
