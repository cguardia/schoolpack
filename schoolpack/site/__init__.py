from zope.interface import implementer

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )

from pyramid.request import Request

from pyramid.events import (
    subscriber,
    ApplicationCreated,
    )

from substanced.content import content
from substanced.root import (
    Root,
    RootPropertySheet
    )

from substanced.catalog import Catalog

from ..interfaces import (
    ISite,
    )


@content(
    'Root',
    icon='icon-home',
    propertysheets=(
        ('', RootPropertySheet),
        ),
    after_create=('after_create', 'after_creation')
    )
@implementer(ISite)
class Site(Root):
    def after_creation(self, inst, registry):
        self.sdi_title = 'School Pack'
        catalog = Catalog()
        self.add_service('catalog', catalog)
        self.update_indexes(registry)
        principals = self.find_service('principals')
        supervisors = principals.add_group('supervisors')
        principals.add_group('teachers')
        principals.add_group('students')
        principals.add_group('tutors')
        self.__acl__.extend([
            (Allow, supervisors, ('sdi.view',)),
            (Allow, Everyone, ('view',)),
            (Allow, Authenticated, ('manage profile',))
            ])

    def update_indexes(self, registry):
        catalog = self['catalog']
        catalog.update_indexes('system', registry=registry, reindex=True)
        catalog.update_indexes('schoolpack', registry=registry, reindex=True)


# update indexes whenever the application is restarted
@subscriber(ApplicationCreated)
def on_application_create(event):
    app = event.app
    registry = app.registry
    req = Request.blank('/')
    req.registry = registry
    root = app.root_factory(req)
    root.update_indexes(registry)


def includeme(config):
    """ Set up application-specific catalog indexes in "schoolpack" category.
    """
    config.add_catalog_index('texts', 'text', 'schoolpack')
    config.add_catalog_index('title', 'field', 'schoolpack')
    config.add_catalog_index('creation_date', 'field', 'schoolpack')
