from django.conf import settings
from base.url_helpers import reverse_hash_target
from base.main_menu import MENUS


class MainMenu(object):
    def __init__(self, request):
        self.request = request

    @staticmethod
    def _reverse_with_target(ctx_item, item_rurl):
        url, target = reverse_hash_target(item_rurl)
        ctx_item['url'] = url
        if target:
            ctx_item['target'] = target

    def _convert_menu(self, menu_in, menu_id, depth):
        ctx_menu = []
        active = False
        menu = getattr(self, menu_in)() if isinstance(menu_in, str) else menu_in

        if not hasattr(self.request, 'active_page'):
            self.request.active_page = ''

        for i, item in enumerate(menu):

            ctx_item = {'name': item['name'], 'class': u'depth_%d' % depth}
            sub_active = False
            if 'submenu' in item:
                item_menu_id = menu_id + str(i)
                ctx_item['submenu'], item_active = self._convert_menu(item['submenu'], item_menu_id + '_sub', depth + 1)
                sub_active |= item_active
                ctx_item['menu_id'] = item_menu_id
                ctx_item['url'] = '#' + item_menu_id
            else:
                self._reverse_with_target(ctx_item, item['rurl'])

            ctx_item['active'] = self.request.active_page == item.get('rurl', None)
            ctx_item['subactive'] = sub_active
            active |= (sub_active or self.request.active_page == item.get('rurl', None))
            ctx_menu.append(ctx_item)
        # TODO: investigate why it's not always a string.
        self.request.active_page = unicode(self.request.active_page)
        return ctx_menu, active


def app_basic(request):
    context = {}
    menu = MENUS['Admin']

    context['main_menu'] = MainMenu(request)._convert_menu(menu, 'menu', 1)[0]
    return context
