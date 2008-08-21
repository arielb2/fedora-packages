from tw.api import Widget, js_function
from tw.jquery import JQuery,jquery_js
from myfedora.lib.app_factory import AppFactory
from pylons import app_globals
from pylons import request
from tg import url

from urlparse import urlparse

class NavigationApp(AppFactory):
    entry_name = 'navigation'

class NavigationWidget(Widget):
    params=[]
    template = 'genshi:myfedora.plugins.apps.templates.navigation'
    javascript = [jquery_js]

    def update_params(self, d):
        super(NavigationWidget, self).update_params(d)
        
        # right now just work with resource views but we should also work with
        # user defined links and other controllers
        rvs = app_globals.resourceviews
        nav = []
        
        url_path = urlparse(request.environ['PATH_INFO']).path
        
        
        for name in rvs.keys():
            view = rvs[name]
            item = {'label': '',
                    'icon': None,
                    'href': '',
                    'state': 'inactive'}
            
            item['label'] = view.display_name
            item['href'] = url('/' + view.entry_name)
            link_path = urlparse(item['href']).path
            if url_path.startswith(link_path):
                item['state'] = 'active'
            
            nav.append(item)
        
        d.update({'navigation_list': nav})
        return d