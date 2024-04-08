from drf_yasg import openapi

type = openapi.Parameter('type', openapi.IN_QUERY,
                         description="specify type of search ['course', 'topic', 'sub_topic', 'question', 'global']",
                         type=openapi.TYPE_STRING)
query = openapi.Parameter('query', openapi.IN_QUERY,
                          description="query for search",
                          type=openapi.TYPE_STRING)
manual_parameters = [type, query]
