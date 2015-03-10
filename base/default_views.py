from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, RedirectView
from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe
from django.utils.http import is_safe_url
from django.shortcuts import render

from base.display_generator import ItemDisplayMixin, BasicPage


class CustomListView(ItemDisplayMixin, ListView):
    """
    This is the main ListView you should use for most lists in the system which
    need to show a grid of data on objects (eg. contractors).

    It generates headers (attributes names) and converts attributes to nice values.
    """
    filter_show_list = True


class CustomDetailView(ItemDisplayMixin, DetailView):
    """
    This is the main DetailView you should use for showing items.

    It generates headers (attributes names) and converts attributes to nice values.
    """
    filter_show_list = False
    template_name = 'common/details.jinja'
    extra_content = None

    def get_context_data(self, **kwargs):
        context = super(CustomDetailView, self).get_context_data(**kwargs)
        context['extra_content'] = self.extra_content
        return context


class CustomTableListView(CustomListView):
    """
    Alternative list view with shows a table rather than a grid
    for each item.
    """
    template_name = 'common/table_list.html'


class EditView(BasicPage):
    """
    basics for edit views.
    """
    template_name = 'common/edit_basic.html'

    def get_form_kwargs(self):
        kwargs = super(EditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class EditModelView(EditView):
    """
    basics for editing/creating a model item.
    """
    pass


def not_built(request, active='index', title='', description=''):
    request.active_page = active
    context = {'title': title, 'description': mark_safe(description)}
    return render(request, 'common/not_built.jinja', context)


class DeleteObject(RedirectView):
    """
    base class that checks if the user has permissions to delete the object
    then deletes that object.
    """
    permanent = False
    reverse_name = None
    perms = []

    def delete(self, pk):
        """
        actual function to delete the object, can be overwritten to alter delete behavior, eg. to just hide.
        """
        item = self.model.objects.get(pk=pk)
        item.delete()

    def post(self, request, *args, **kwargs):
        self.delete(kwargs['pk'])
        return super(DeleteObject, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse(self.reverse_name)


class ModalMixin(object):
    """
    Simple mixin to add/edit data on a bootstrap modal
    You need to specify a template for modal using modal_template_name attribute.
    If the request is via ajax it renders the form on modal template, otherwise renders the normal view.
    """

    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            self.template_name = getattr(self, 'modal_template_name', 'common/modals/form_modal.jinja')
        return super(ModalMixin, self).dispatch(*args, **kwargs)

