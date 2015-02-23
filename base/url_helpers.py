from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.utils.log import getLogger

logger = getLogger('django')

# for now lets assume exception muting here follows 
# JINJA2_MUTE_URLRESOLVE_EXCEPTIONS
MUTE_RESOLVE_EXC = getattr(settings, "JINJA2_MUTE_URLRESOLVE_EXCEPTIONS", False)


def reverse_hash(rurl):
    """
    Reverse accounting for hash arguments which are added to the end of generated urls.
    """
    return reverse_hash_target(rurl)[0]


def reverse_hash_target(rurl):
    """
    Reverse accounting for hash arguments which are added to the end of generated urls.

    Returns both url and the target
    """
    url_dict = rurl if isinstance(rurl, dict) else {'viewname': rurl}
    url_base = u'%s'
    target = None
    if '#' in url_dict['viewname']:
        assert url_dict['viewname'].count('#') == 1, 'use only one # to specify target'
        url_dict['viewname'], target = url_dict['viewname'].split('#')
        url_base = u'%%s#%s' % target
    try:
        return url_base % reverse(**url_dict), target
    except NoReverseMatch, e:
        if not MUTE_RESOLVE_EXC:
            raise e
        else:
            logger.warn(u'Warning: no reverse for "%s"', url_dict.get('viewname', 'unknown view'))
