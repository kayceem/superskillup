from drf_yasg import openapi
from app.app_admin.serializers import AdminSerializer


class AdminResponse():
    @staticmethod
    def response_dict(many):
        reponse_example = {
            "status_code": 1,
            "status_message": "string",
            "data": {
                "access_token": "string"
            },
            "page": {},
            "error": {}
        }
        return reponse_example if not many else [reponse_example]

    @classmethod
    def response(cls, many=False):
        return openapi.Response(
            description="",
            schema=AdminSerializer(many=many),
            examples={
                "application/json": AdminResponse.response_dict(many)}
        )
