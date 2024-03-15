from app.api import api
from app.app_admin.accessor import AdminAccessor
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class Admin:

    def __init__(self, admin):
        self.admin = admin

    @staticmethod
    def get_user_by_id(admin_id):
        return AdminAccessor.get_admin(id=admin_id)

    @staticmethod
    def get_admin_by_username(username):
        return AdminAccessor.get_admin(username=username)

    def generate_auth_token(self):
        refresh = RefreshToken.for_user(self.admin)
        return str(refresh.access_token)


    @classmethod
    def login(cls, username, raw_password):
        admin = cls.get_admin_by_username(username)
        if not admin:
            return api.ADMIN_USER_NOT_FOUND, None

        if not admin.check_password(raw_password):
            return api.INVALID_PASSWORD, None
        return api.SUCCESS, cls(admin).generate_auth_token()