__author__ = 'codeadict'

import os

from django.conf import settings
from django.template import TemplateDoesNotExist


def load_mustache_template_source(template_name):
    for template_dir in settings.TEMPLATE_DIRS:
        template_path = os.path.join(template_dir, template_name)
        if os.path.exists(template_path):
            return open(template_path).read()

    raise TemplateDoesNotExist
