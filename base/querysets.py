from django.db import models


class BaseRequestQueryset(models.QuerySet):
    """
    Default parent for all TC models' default queryset. All managers should get a queryset which inherit from this
    class, the queryset should implement at least request_qs.

    The general usage is

    class CustomQueryset(BaseRequestQueryset):
            request_qs(self, request):
                return self.filter(...)

    class MyModel(models.Model):
        objects = CustomQueryset.as_manager()
        ...
    """
    def request_qs(self, request):
        """
        Filter to the standard qs of items a request would expect to see.

        :param request: django request object
        :return: queryset filtered such that it is suitable response to this request.
        """
        raise NotImplementedError('%s manager/queryset has not implemented the "request_qs" method' % self.model)

    def request_full_qs(self, request):
        """
        Filter to the full qs of items which should ever be returned from a request.

        By default this just returns not normal request queryset.

        :param request: django request object
        :return: queryset
        """
        return self.request_qs(request)

    def request_superuser_qs(self, request):
        """
        Get request_qs unless the user is a superuser in which case return all.
        :param request: django request object
        :return: qs
        """
        if request.user.is_superuser:
            return self
        else:
            return self.request_qs(request)