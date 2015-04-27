from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _

from djgeojson.views import GeoJSONLayerView

from base.models import Label
from base.default_views import CustomListView, CustomDetailView, EditModelView


class ListFilterMixin(object):
    """
    Mixin for filtering and sorting lists
    """
    search_form = None

    def get_filter_form(self):
        if not self.search_form:
            return None

        return self.search_form(request=self.request, data=self.request.GET or None)

    def get_queryset(self):
        queryset = super(ListFilterMixin, self).get_queryset()
        form = self.get_filter_form()
        if form and form.data:
            if form.is_valid():
                queryset = form.apply(queryset)
            else:
                queryset = queryset.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListFilterMixin, self).get_context_data(**kwargs)
        context['search_form'] = self.get_filter_form()
        return context
