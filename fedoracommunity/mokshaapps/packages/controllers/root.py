from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer

from repoze.what.predicates import not_anonymous
from tg import expose, tmpl_context, require, request

class UserPkgsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.userpkgs_table_widget'

class BuildsContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('right-content-column',
                        MokshaApp('Quick Links', 'fedoracommunity.quicklinks')),
              Category('left-content-column',
                       MokshaApp('Builds', 'fedoracommunity.builds/table', params={"rows_per_page": 10, "filters":{}}))]

    def update_params(self, d):
        super(BuildsContainer, self).update_params(d)

builds_container = BuildsContainer('builds')
user_pkgs_grid = UserPkgsGrid('usrpkgs_table')

class RootController(Controller):

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.userpackages')
    @require(not_anonymous())
    def mypackages(self, owner=5, maintainer=3, watcher=False):
        username = request.identity['repoze.who.userid']

        categories = []
        if owner:
            cat = {'label': 'Packages I Own',
                   'rows_per_page': owner,
                   'filters':{'owner': True, 'u':username, 'eol': False}
                  }
            categories.append(cat)

        if maintainer:
            cat = {'label': 'Packages I Maintain',
                   'rows_per_page': maintainer,
                   'filters':{'approveacls': True, 'commit': True,'u':username, 'eol': False}
                  }
            categories.append(cat)

        if watcher:
            cat = {'label': 'Packages I Watch',
                   'rows_per_page': watcher,
                   'filters':{'watchcommits': True, 'watchbugzilla': True,'u':username, 'eol': False}
                  }
            categories.append(cat)

        tmpl_context.widget = user_pkgs_grid
        return {'categories': categories}

    # do something for index, this should be the container stuff
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {
            'filters': {'package': kwds.get('package', kwds.get('pkg', kwds.get('p')))}
        }

        tmpl_context.widget = builds_container
        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def name(self, pkg_name, **kwds):

        kwds.update({'p': pkg_name})
        return self.index(**kwds)

    @expose('mako:fedoracommunity.mokshaapps.builds.templates.table')
    def table(self, uid="", rows_per_page=5, filters={}):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = builds_grid
        return {'filters': filters, 'uid':uid, 'rows_per_page':rows_per_page}