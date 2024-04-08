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
                "name": "user-gpt-review",
                "description": "Endpoint for user and gpt review interaction."
            },
            {
                "name": "search",
                "description": "Endpoint for searching course, topic, sub topic and questions."
            },
            {
                "name": "admin-review",
                "description": "Endpoints for admin and review(for question answer) interaction."
            },
            {
                "name": "user-review",
                "description": "Endpoints for user and review(for question answer) interaction."
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
