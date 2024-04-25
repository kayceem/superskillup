from rest_framework.decorators import api_view, authentication_classes, parser_classes
from app.api.response_builder import ResponseBuilder
from app.shared.pagination import paginate
from app.sub_topic.serializers import SubTopicSerializer
from app.api import api
from app.sub_topic.sub_topic import SubTopic
from app.shared.authentication import AdminAuthentication
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-sub-topic'], method='get', responses={200: SubTopicSerializer(many=True)})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_sub_topics_by_topic(request, topic_id):
    """
    Get sub_topics of topic
    """
    response_builder = ResponseBuilder()
    sub_topics = SubTopic.get_sub_topics_by_topic(topic_id=topic_id)
    if not sub_topics:
        return response_builder.get_404_not_found_response(api.SUB_TOPIC_NOT_FOUND)
    paginated_sub_topics, page_info = paginate(sub_topics, request)
    serializer = SubTopicSerializer(paginated_sub_topics, many=True)
    return response_builder.get_200_success_response("SubTopics found", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-sub-topic'], method='get', responses={200: SubTopicSerializer})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_sub_topic_by_id(request, id):
    """
    Get the sub_topic by id
    """

    response_builder = ResponseBuilder()
    sub_topic = SubTopic.get_sub_topic_by_id(sub_topic_id=id)
    if not sub_topic:
        return response_builder.get_404_not_found_response(api.SUB_TOPIC_NOT_FOUND)
    serializer = SubTopicSerializer(sub_topic)
    return response_builder.get_200_success_response("SubTopic found", serializer.data)


@swagger_auto_schema(tags=['admin-sub-topic'], method='post', request_body=SubTopicSerializer, responses={201: SubTopicSerializer})
@api_view(['POST'])
@authentication_classes([AdminAuthentication])
@parser_classes([MultiPartParser])
def create_sub_topic(request):
    """
    Create a SubTopic.
    """

    response_builder = ResponseBuilder()
    video = request.data.get('video', None)
    if video:
        video_length = SubTopic.get_video_length(video)
        request.data['video_length'] = video_length
    serializer = SubTopicSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("SubTopic created successfully", serializer.data)


@swagger_auto_schema(tags=['admin-sub-topic'], methods=['put', 'patch'], request_body=SubTopicSerializer, responses={201: SubTopicSerializer})
@api_view(['PATCH', 'PUT'])
@authentication_classes([AdminAuthentication])
@parser_classes([MultiPartParser])
def update_sub_topic(request, id):
    """
    Update the provided sub_topic
    """

    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    sub_topic = SubTopic.get_sub_topic_by_id(sub_topic_id=id)
    if not sub_topic:
        return response_builder.get_404_not_found_response(api.SUB_TOPIC_NOT_FOUND)
    serializer = SubTopicSerializer(sub_topic, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("SubTopic updated successfully", serializer.data)


@swagger_auto_schema(tags=['admin-sub-topic'], method='delete', request_body=SubTopicSerializer)
@api_view(['DELETE'])
@authentication_classes([AdminAuthentication])
def delete_sub_topic(request, id):
    """
    Delete sub_topic
    """
    response_builder = ResponseBuilder()
    sub_topic = SubTopic.get_sub_topic_by_id(sub_topic_id=id)
    if not sub_topic:
        return response_builder.get_404_not_found_response(api.SUB_TOPIC_NOT_FOUND)
    deleted = SubTopic.delete_sub_topic(sub_topic)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
