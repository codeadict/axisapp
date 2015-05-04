from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from base.display_generator import BasicPage


class TrackingView(BasicPage, TemplateView):
    title = _('Employee Tracking')
    active_page = 'employee-tracking'
    template_name = 'tracking/map.jinja'
    button_menu = [
        {'name': _('Work Report'), 'urlfunc': 'fullscreen_url'},
        {'name': _('FullScreen Map'), 'urlfunc': 'fullscreen_url', 'classes': 'map-go-fullscreen'},
    ]

    def fullscreen_url(self):
        return 'javascript:void(0);'

    def get_context_data(self, **kwargs):
        context = super(TrackingView, self).get_context_data(**kwargs)
        context['full_width'] = True
        return context

tracking_view = TrackingView.as_view()
