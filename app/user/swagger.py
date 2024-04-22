from drf_yasg import openapi
from app.user.serializers import UserSerializer


class UserResponse():
    @staticmethod
    def response_dict():
        message = {"message": "string"}
        reponse_example = {
            "status_code": 1,
            "status_message": "string",
            "data": {
                **message
            },
            "page": {},
            "error": {}
        }
        return reponse_example

    @classmethod
    def response(cls):
        return openapi.Response(
            description="",
            examples={
                "application/json": UserResponse.response_dict()}
        )


class LoginResponse():

    @staticmethod
    def response_dict():
        message = {"message": "string"}
        token = {"access_token": "string"}
        role = {"role": "string"}
        info = {"info": "dict"}
        reponse_example = {
            "status_code": 1,
            "status_message": "string",
            "data": {
                **message,
                **token,
                **role,
                **info
            },
            "page": {},
            "error": {}
        }
        return reponse_example

    @classmethod
    def response(cls):
        return openapi.Response(
            description="",
            examples={
                "application/json": LoginResponse.response_dict()}
        )
