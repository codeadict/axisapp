__author__ = "malbalat85"


#TODO: This must be into base, but i'm awaiting orders from the boss @dmedina
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
