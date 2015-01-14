from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from axisapp.company.models import VOID_TRANSCODE


class CustomLocaleMiddleware(LocaleMiddleware):
    """
    Custom locale that takes trans_code from company industry to add specific
    terms for this kind of industry jargon.
    """
    def process_request(self, request):
        check_path = self.is_language_prefix_patterns_used()
        language = translation.get_language_from_request(request, check_path=check_path)

        if request.user.is_authenticated() and request.user.branch:
            trans_code = request.user.branch.company.industry.trans_code
            if trans_code not in [None, VOID_TRANSCODE]:
                language = language[:2] + '-' + trans_code

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
