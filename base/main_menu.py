# This Python file uses the following encoding: utf-8
from django.utils.translation import ugettext_lazy as _


MENUS = {
    'Admin': [
        {'name': _('Tablero de Mando'), 'rurl': 'index'},
        {'name': _('Clientes'), 'submenu': [
            {'name': _('Lista'), 'rurl': 'client-list', 'perms': []},
            {'name': _('Mapa'), 'rurl': 'client-map', 'perms': []},
        ]},
        {'name': _('Logistica'), 'submenu': [
            {'name': _('Distribucion'), 'submenu': [
                {'name': _('Asignaciones Preventa'), 'rurl': 'index', 'perms': []},
                {'name': _('Seguimiento Censadores/Prevendedores'), 'rurl': 'index', 'perms': []},
            ]},
            {'name': _('Inventarios'), 'submenu': [
                    {'name': _('Productos'), 'rurl': 'index', 'perms': []},
            ]},
        ]},
        {'name': _('Ventas'), 'submenu': [
            {'name': _('Pedidos'), 'rurl': 'index', 'perms': []},
        ]},

    ],
}