from app.user.accessor import UserAccessor
from rest_framework_simplejwt.tokens import RefreshToken
from app.api import api
from app.utils.hashing import check_password

class User:

    def __init__(self, user):
        self.user = user

    @staticmethod
    def get_user_by_id(user_id):
        return UserAccessor.get_user(id=user_id)

    @staticmethod
    def get_user_by_email(email):
        return UserAccessor.get_user(email=email)

    def generate_auth_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    @classmethod
    def login(cls, email, raw_password):
        user = cls.get_user_by_email(email)
        if not user:
            return api.USER_NOT_FOUND, None
        if not user.is_verified:
            return api.USER_NOT_VERIFIED, None
        borrower_obj = cls(user)

        if not check_password(raw_password, user.password):
            return api.INVALID_PASSWORD, None

        return api.SUCCESS, borrower_obj.generate_auth_token()
