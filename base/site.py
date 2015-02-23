__author__ = 'codeadict'
from django.contrib.admin.sites import AdminSite


class AdminMixin(object):
    """Mixin for AdminSite to allow custom dashboard views."""

    def __init__(self, *args, **kwargs):
        return super(AdminMixin, self).__init__(*args, **kwargs)



class SitePlus(AdminMixin, AdminSite):
    """
    A Django AdminSite with the AdminMixin to allow registering custom
    dashboard view.
    """
