"""

To activate custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'biorepo-portal.menu.CustomMenu'
"""

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for biorepo-portal admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.AppList(
                _('Models'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            items.MenuItem(
                _('Protocol Management'),
                children=[
                    items.MenuItem('Add User to Protocol', '/brp_admin/new_protocol_usr/'),
                    items.MenuItem('Add User Credentials to Protocol Group', '/brp_admin/fn_in_progress/'),
                    items.MenuItem('Add Data Source to protocol', '/brp_admin/fn_in_progress/'),

                ]
            ),
            items.MenuItem(
                _('BRP Management'),
                children=[
                    items.MenuItem('cache subjects', '/brp_admin/cache_subjects/'),
                    items.MenuItem('toggle maintenance', '/brp_admin/fn_in_progress/'),
                    items.MenuItem('cache ehb labels', '/brp_admin/cache_labels/'),
                ]
            ),
            items.MenuItem(
                _('User Management'),
                children=[
                    items.MenuItem('re-activate user', '/brp_admin/reactivate_user/'),
                    items.MenuItem('update user nautilus credentials', '/brp_admin/update_nautilus_credentials/'),
                    items.MenuItem('update user REDCap credentials', '/brp_admin/fn_in_progress/'),
                ]
            ),
            items.MenuItem(
                _('BRP/EHB Useful links'),
                children=[
                    items.MenuItem('BRP EHB Gist', '/brp_admin/fn_in_progress/'),
                    items.MenuItem('BRP read the docs', 'http://biorepository-portal.readthedocs.io/en/latest/'),
                    items.MenuItem('BRP user guide', '/brp_admin/fn_in_progress/'),
                    items.MenuItem('BRP CHOP wiki', 'https://wiki.chop.edu/pages/viewpage.action?pageId=131957293'),
                    items.MenuItem('EHB CHOP wiki', 'https://wiki.chop.edu/display/CBMIDI/eHonest+Broker'),
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
