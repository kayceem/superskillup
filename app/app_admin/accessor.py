from app.utils.utils import get_or_none
from django.contrib.auth.models import User


class AdminAccessor:

    @classmethod
    def get_admin(cls, **kwargs):
        return get_or_none(User, **kwargs)

    @classmethod
    def get_admins_from_ids(cls, admin_ids) -> list[User] | None:
        return User.objects.filter(id__in=admin_ids).all()
