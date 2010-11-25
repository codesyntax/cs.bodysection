from zope.interface import Interface, implements
from zope.component import queryMultiAdapter

from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavigationRoot


class INavigationRootContent(Interface):
    def section_content_body_class():
        """ return a unique section class based on the id of the nearer child of a 
        INavigationRoot item parent of the current context
        """

    def is_navigation_root_or_default_page():
        """ return whether the current object is the navigation
            root element or the default page of a navigation root
            item. This is similar to @@ploneview/isPortalOrPortalDefaultPage method
        """

class NavigationRootContent(BrowserView):
    implements(INavigationRootContent)

    def section_content_body_class(self):
        portal_state = queryMultiAdapter((self.context, self.request),
                                         name='plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        root_path_length = len(navigation_root_path)
        path_name = '-'.join(self.context.getPhysicalPath())[root_path_length:]
        if path_name != '-':
            return 'content-section' + path_name
        else:
            return ''

    @memoize
    def is_navigation_root_or_default_page(self):
        context = aq_inner(self.context)
        context_state = getMultiAdapter(
            (context, self.request), name=u'plone_context_state')
        if context_state.is_default_page():
            return INavigationRoot.providedBy(aq_parent(context))
        else:
            return INavigationRoot.providedBy(context)
        
        
        