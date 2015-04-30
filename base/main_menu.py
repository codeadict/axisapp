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
                {'name': _('Asignaciones Preventa'), 'rurl': 'presales-client-distribution', 'perms': []},
                {'name': _('Seguimiento Censadores/Prevendedores'), 'rurl': 'index', 'perms': []},
            ]},
            {'name': _('Inventarios'), 'submenu': [
                    {'name': _('Productos'), 'rurl': 'index', 'perms': []},
            ]},
        ]},
        {'name': _('Ventas'), 'submenu': [
            {'name': _('Pedidos'), 'rurl': 'index', 'perms': []},
        ]},
        {'name': _('Products'), 'submenu': [
            {'name': _('Inventory'), 'rurl': 'product-list', 'perms': []},
        ]},
        {'name': _('HHRR'), 'submenu': [
            {'name': _('Employees'), 'rurl': 'employee-list', 'perms': []},
            {'name': _('Employee Map'), 'rurl': 'employee-map', 'perms': []},
        ]},
        {'name': _('Configuracion'), 'submenu': [
            {'name': _('Importar Datos'), 'rurl': 'import', 'perms': []},
            {'name': _('Inventory'), 'submenu': [
                {'name': _('Product Categories'), 'rurl': 'product-category-details', 'perms': []},
            ]},
        ]},
    ],
}
