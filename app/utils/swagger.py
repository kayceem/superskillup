from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "admin-auth",
                "description": "Endpoint for admin authentication."
            },
            {
                "name": "admin-assignment",
                "description": "Endpoints for admin and assignment interaction."
            },
            {
                "name": "admin-course",
                "description": "Endpoints for admin and course interaction."
            },
            {
                "name": "admin-gpt-review",
                "description": "Endpoint for admin and gpt review interaction."
            },
            {
                "name": "admin-review",
                "description": "Endpoints for admin and review(manager feedback) interaction."
            },
            {
                "name": "admin-question",
                "description": "Endpoints for admin and question interaction."
            },
            {
                "name": "admin-answer",
                "description": "Endpoints for admin and question answer interaction."
            },
            {
                "name": "admin-sub-topic",
                "description": "Endpoints for admin and sub topic interaction."
            },
            {
                "name": "admin-topic",
                "description": "Endpoints for admin and topic interaction."
            },
            {
                "name": "admin-user",
                "description": "Endpoint for admin and user interaction."
            },
            {
                "name": "admin-user-assignment",
                "description": "Endpoints for admin and user assignment interaction."
            },
            {
                "name": "user-auth",
                "description": "Endpoint for user authentication."
            },
            {
                "name": "user-gpt-review",
                "description": "Endpoint for user and gpt review interaction."
            },
            {
                "name": "user-review",
                "description": "Endpoints for user and review(manager feedback) interaction."
            },
            {
                "name": "user-answer",
                "description": "Endpoints for user and question answer interaction."
            },
            {
                "name": "user-assignment",
                "description": "Endpoints for user and assignment interaction."
            },
            {
                "name": "search",
                "description": "Endpoint for searching course, topic, sub topic and questions."
            },
            {
                "name": "tags",
                "description": "Endpoints for tags"
            },
            {
                "name": "admin",
                "description": "Endpoints for admin auth."
            },
            {
                "name": "user",
                "description": "Endpoints for user auth and signup."
            },
        ]

        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title="Superskill up",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)
