import logging

from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from task import get_context_hull_by_areas

from base.default_views import CustomListView, ModalMixin
from censo.models import PresalesDistribution
from censo.forms import GenerateDistributionForm

log = logging.getLogger(__name__)


class DistributionList(CustomListView):
    """
    View to list and map distribution models as well as generating new ones
    """
    template_name = 'distribution/list.jinja'
    active_page = 'presales-client-distribution'
    model = PresalesDistribution
    perms = []
    # detail_view = ''
    display_items = [
        'name',
        'assigned_seller',
    ]
    button_menu = [
        {
            'name': _('Generate New Distribution'), 'rurl': 'generate-distribution', 'data':
            {'toggle': 'crud-modal', 'title': _('Generate Pre-Sales Distribution')}
        },
    ]

    def get_search_form(self):
        return NotImplementedError

    def get_queryset(self):
        qs = super(DistributionList, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributionList, self).get_context_data(**kwargs)
        return context


distribution_list = DistributionList.as_view()


class GenerateDistribution(ModalMixin, FormView):
    """
    Launches a modal and generates a distribution based on area_id and number of points per distribution polygon
    """
    form_class = GenerateDistributionForm
    modal_template_name = 'common/modals/generate_distribution_modal.jinja'
    perms = []

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.form.is_valid():
            # TODO: Here we generate the distribution
            # Just for test
            #self.get_context_hull_by_areas.delay(2, 50)
            area = request.post['area']
            points_per_polygon = request.post['points_per_polygon']
            get_context_hull_by_areas.delay(int(area), int(points_per_polygon))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('presales-client-distribution')


distribution_generate = GenerateDistribution.as_view()