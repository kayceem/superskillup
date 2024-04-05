from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication, CombinedAuthentication
from app.tag.tag import Tag
from app.api.response_builder import ResponseBuilder
from app.tag.serializer import TagSerializer
from app.api import api


@api_view(["GET"])
@authentication_classes([CombinedAuthentication])
def get_tag_by_id(request, id):
    response_builder = ResponseBuilder()
    tag = Tag.get_tag_by_id(id)
    if not tag:
        return response_builder.get_404_not_found_response(api.TAG_NOT_FOUND)
    serializer = TagSerializer(tag)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([CombinedAuthentication])
def get_all_tags(request):
    response_builder = ResponseBuilder()
    tags = Tag.get_all_tags()
    if not tags:
        return response_builder.get_404_not_found_response(api.TAG_NOT_FOUND)
    serializer = TagSerializer(tags, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
