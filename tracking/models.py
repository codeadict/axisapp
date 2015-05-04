from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models

from swampdragon.models import SelfPublishModel
from swampdragon.serializers.model_serializer import ModelSerializer

from sdauth.models import User



class UserTrackingSerializer(ModelSerializer):
    """
    Serializes user activity data
    """
    class Meta:
        model = 'tracking.UserTracking'
        publish_fields = ('user', 'date_time', 'lat', 'lgn')


class UserTracking(SelfPublishModel, models.Model):
    """
    Database table for employee tracking
    """
    serializer_class = UserTrackingSerializer
    user = models.ForeignKey(User, verbose_name=_('User'))
    date_time = models.DateTimeField(_('Datetime'), auto_now_add=True)
    lat = models.FloatField(_('Latitude'))
    lgn = models.FloatField(_('Longitude'))

    class Meta:
        verbose_name = _('User Position')
        verbose_name_plural = _('User positions')

    def __unicode__(self):
        return '%s %s %s' % (self.user, ugettext('on'), self.date_time)