from drf_yasg import openapi
from app.user.serializers import UserSerializer


class UserResponse():
    @staticmethod
    def response_dict(is_message):
        message = {"message": "string"}
        token = {"access_token": "string"}
        if is_message:
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
        reponse_example = {
            "status_code": 1,
            "status_message": "string",
            "data": {
                **token
            },
            "page": {},
            "error": {}
        }
        return reponse_example

    @classmethod
    def response(cls, message=True):
        return openapi.Response(
            description="",
            examples={
                "application/json": UserResponse.response_dict(message)}
        )
