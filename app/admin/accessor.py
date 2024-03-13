from app.utils.utils import get_or_none
from django.contrib.auth.models import User


class AdminAccessor:

    @classmethod
    def get_admin(cls, **kwargs):
        return get_or_none(User, **kwargs)
