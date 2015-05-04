from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter

from tracking.models import UserTrackingSerializer
from tracking.models import UserTracking


class UserTrackingRouter(ModelRouter):
    """
    Route for user tracking
    """
    route_name = 'user-tracking'
    serializer_class = UserTrackingSerializer
    model = UserTracking

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

route_handler.register(UserTrackingRouter)