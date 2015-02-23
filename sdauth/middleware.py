import re
import pytz

from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.conf import settings


EXEMPT_URLS = ['^/login/$', '^/signup/$', '^/[-\w]+/password/reset/', '^/admin',
               '^/accounts', '^/api/', '^/__debug__', '^/setup/create_company', '^/captcha/']

EXEMPT_URLS += ['^/media/public']
EXEMPT_URLS_RE = [re.compile(bit) for bit in EXEMPT_URLS]

class SDAuthMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), "Auth middleware required."

        if not request.user.is_authenticated():
            # Anonymous users
            if any(m.match(request.path) for m in EXEMPT_URLS_RE):
                if '/accounts/profile/' not in request.path:
                    return

            raise PermissionDenied


        if request.user.is_superuser:
            # Superuser without agency
            su_allowed = ('/admin/', '/api/', '/setup/create_agency/', '/captcha/image/', '/django-rq/')
            if any(request.path.startswith(s) for s in su_allowed):
                return
