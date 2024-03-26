from app.ManagerFeedback.ManagerFeedback import ManagerFeedback
from rest_framework.decorators import api_view, authentication_classes
from app.api.response_builder import ResponseBuilder
from app.api import api
from app.shared.authentication import AdminAuthentication


# @api_view(["GET"])
# @authentication_classes([AdminAuthentication])
# def get_all_feedback(request):
