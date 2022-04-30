# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Clase para generar el menu

"""


from .models import Menu

from backend_apps.utils.security import UserToken

# reload(sys)
# sys.setdefaultencoding('utf-8')
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils.text import capfirst


class Menus:
    """
            Clase que permite renderizar los menus.
    """
    menu_module = ''  # Variable para indicar el entorno
    menu_list = []  # Variable que contiene los menus
    menu_item_list = {}  # Variable que contien los items del menu

    # Método para cargar en variables los menús
    @staticmethod
    def load(request):
        """
        Carga el menu del usuario

        Entrada::

                menu_module=BACKEND

        Salida::

                menu_item_list[menu]
    """
        Menus.menu_list = []
        Menus.menu_item_list = {}

        user = request.user

        permission_list = []

        if not request.user.is_superuser:
            try:
                groups = list(col['id'] for col in Group.objects.values('id').filter(user=user))
                permission_list = Permission.objects.filter(group__in=groups).distinct()
            except:
                # headquar=Headquar.objects.filter(userheadquar__user__id=request.user.id).distinct().first()
                pass

        if request.user.is_superuser:
            permission_list = []  # si es uperuser mostrarme todo los menús

        # permission_list = []
        # obtengo los hijos y luego saco sus padres, esto es para no mostrar un
        # menu sin items
        menu_item_list_t = Menu.objects.filter(Q(permission__in=permission_list) | Q(
            id__isnull=True if permission_list else False), is_active=True).order_by("pos")
        Menus.menu_list = Menu.objects.filter(
            menu__in=menu_item_list_t, is_active=True).order_by("pos").distinct()
        # print Menus.menu_list
        if Menus.menu_list:
            for menu in Menus.menu_list:
                Menus.menu_item_list[menu.title] = Menu.objects.filter(
                    Q(permission__in=permission_list) | Q(
                        id__isnull=True if permission_list else False), parent_id=menu.id,
                    is_active=True).order_by(
                    "pos")  # .lower().replace(" ","_")
        # print Menus.menu_item_list
        return ""

    # Metodo para renderizar el menu de escritorio
    @staticmethod
    def desktop(request):
        """
        Método para renderizar el menu de escritorio
    """
        html = ''
        route = request.path
        if Menus.menu_list:
            html = html + '<ul class="nav">'

            for main in Menus.menu_list:
                active = ('active' if main.url == route else '')
                html = html + '<li class="%s">%s</li>\n' % (
                    active, Menus.linkdf(main.url, main.title, main.icon))
            html = html + '</ul>\n'
        return html

    # metodo privado
    @staticmethod
    def linkdf(action, text, icon):  # , attrs = None, icon='', loadAjax=True
        action = ('/%s' % action if action != '#' else '#')
        texti = ""
        if icon:
            texti = '<i class="%s fa-lg"></i>' % icon
        html = '<a href="%s"  class="dw-spinner dw-ajax main-menu-link" data-filter="sub-menu-%s" >%s %s</a>\n' % (
            action, text.lower().replace(" ", "_"), texti, _("%s" % text))
        return html

    # metodo privado
    @staticmethod
    def link(action, text, icon):  # , attrs = None, icon='', loadAjax=True
        action = ('/%s' % action if action != '#' else '#')
        texti = ""
        if icon:
            texti = '<i class="%s "></i>' % icon
        html = '<a href="%s">%s %s</a>\n' % (
            action, texti, capfirst(_("%s" % text)))
        return html

    # metodo privado
    @staticmethod
    def link_side(action, text, icon):  # , attrs = None, icon='', loadAjax=True
        action = ('/%s' % action if action != '#' else '#')
        texti = ""
        if icon:
            texti = '<i class="%s fa-lg"></i>' % icon
        html = '<a href="%s"  class="dw-spinner dw-ajax subnav2" >%s <i class="icon-chevron-right"></i>%s</a>\n' % (
            action, texti, _("%s" % text))
        return html

    # metodo privado
    @staticmethod
    # , attrs = None, icon='', loadAjax=True
    def linknoajax(action, text, icon):
        action = ('/%s' % action if action != '#' else '#')
        texti = ""
        if icon:
            texti = '<i class="%s fa-lg"></i>' % icon
        html = '<a href="%s"  class="dw-spinner" >%s %s</a>\n' % (
            action, texti, _("%s" % text))
        return html

    # metodo privado
    @staticmethod
    def linkphone(action, text, icon):  # , attrs = None, icon='', loadAjax=True
        action = ('/%s' % action if action != '#' else '#')
        texti = ""
        if icon:
            texti = '<i class="%s fa-lg"></i>' % icon
        html = '<a href="%s" class="dropdown-toggle" data-toggle="dropdown">%s %s</a>\n' % (
            action, texti, text)
        return html

    # Método para listar los items en el backend
    @staticmethod
    def desktop_items(request):
        """
        Metodo para listar los items del menu de escritorio
    """
        html = ''
        route = request.path
        for menu, items in Menus.menu_item_list.iteritems():
            html = html + \
                   '<div id="sub-menu-%s" class="subnav hidden">\n' % menu.lower().replace(
                       " ", "_")
            html = html + '<ul class="nav nav-pills">\n'

            if menu in Menus.menu_item_list:
                for item in Menus.menu_item_list[menu]:
                    active = ('active' if item.url.strip(
                        "/") == route.strip("/") else '')
                    html = html + '<li class="%s">%s</li>\n' % (
                        active, Menus.link(item.url, item.title, item.icon))
            html = html + '</ul>\n'
            html = html + '</div>\n'
        return html

    # Método para renderizar el menú de dispositivos móviles
    @staticmethod
    def view(request):
        """
        Metodo para renderizar el menu de dispositivos moviles
    """
        html = ''
        route = request.path
        if Menus.menu_list:
            html = html + '<ul class="nav navbar-nav">\n'
            for main in Menus.menu_list:
                text = '%s<b class="caret"></b>' % capfirst(_("%s" % main.title))
                html = html + '<li class="dropdown">\n'
                html = html + Menus.linkphone('#', text, main.icon)
                if main.title in Menus.menu_item_list:
                    html = html + '<ul class="dropdown-menu">\n'
                    for item in Menus.menu_item_list[main.title]:
                        active = ('active' if item.url.strip("/") == route.strip("/") else '')
                        html = html + '<li class="%s">%s</li>\n' % (
                            active, Menus.link(item.url, item.title, item.icon))
                    html = html + '</ul>\n'
                html = html + '</li>\n'
            html = html + '</ul>\n'
        return html

    # Método para listar los items en el sidebar
    @staticmethod
    def side_items(request):
        """
        Metodo para listar los items del menu del sidebar
    """
        html = ''
        route = request.path
        for menu, items in Menus.menu_item_list.iteritems():

            if menu in Menus.menu_item_list:
                for item in Menus.menu_item_list[menu]:
                    active = ('active' if item.url.strip(
                        "/") == route.strip("/") else '')
                    html = html + '<li class="%s">%s</li>\n' % (
                        active, Menus.link_side(item.url, item.title, item.icon))

        return html
