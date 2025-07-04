from rest_framework.decorators import api_view, authentication_classes
from app.api.response_builder import ResponseBuilder
from app.shared.pagination import paginate
from app.topic.serializers import TopicSerializer
from app.api import api
from app.topic.topic import Topic
from app.shared.authentication import AdminAuthentication
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-topic'], method='get', responses={200: TopicSerializer(many=True)})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_topics_by_course(request, course_id):
    """
    Get topics of course
    """
    response_builder = ResponseBuilder()
    topics = Topic.get_topics_by_course(course_id=course_id)
    if not topics:
        return response_builder.get_200_fail_response(api.TOPIC_NOT_FOUND, result=[])
    paginated_topics, page_info = paginate(topics, request)
    serializer = TopicSerializer(paginated_topics, many=True)
    return response_builder.get_200_success_response("Topics found", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-topic'], method='get', responses={200: TopicSerializer})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_topic_by_id(request, id):
    """
    Get the topic by id
    """

    response_builder = ResponseBuilder()
    topic = Topic.get_topic_by_id(topic_id=id)
    if not topic:
        return response_builder.get_404_not_found_response(api.TOPIC_NOT_FOUND)
    serializer = TopicSerializer(topic)
    return response_builder.get_200_success_response("Topic found", serializer.data)


@swagger_auto_schema(tags=['admin-topic'], method='post', request_body=TopicSerializer, responses={201: TopicSerializer})
@api_view(['POST'])
@authentication_classes([AdminAuthentication])
def create_topic(request):
    """
    Create a Topic.
    """

    response_builder = ResponseBuilder()
    serializer = TopicSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Topic created successfully", serializer.data)


@swagger_auto_schema(tags=['admin-topic'], methods=['patch', 'put'], request_body=TopicSerializer, responses={201: TopicSerializer})
@api_view(['PATCH', 'PUT'])
@authentication_classes([AdminAuthentication])
def update_topic(request, id):
    """
    Update the provided topic
    """

    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    topic = Topic.get_topic_by_id(topic_id=id)
    if not topic:
        return response_builder.get_404_not_found_response(api.TOPIC_NOT_FOUND)
    serializer = TopicSerializer(topic, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Topic updated successfully", serializer.data)


@swagger_auto_schema(tags=['admin-topic'], method='delete', request_body=TopicSerializer)
@api_view(['DELETE'])
@authentication_classes([AdminAuthentication])
def delete_topic(request, id):
    """
    Delete topic
    """
    response_builder = ResponseBuilder()
    topic = Topic.get_topic_by_id(topic_id=id)
    if not topic:
        return response_builder.get_404_not_found_response(api.TOPIC_NOT_FOUND)
    deleted = Topic.delete_topic(topic)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
