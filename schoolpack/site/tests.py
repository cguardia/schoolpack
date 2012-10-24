import unittest
from pyramid import testing


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(autocommit=False)

    def tearDown(self):
        testing.tearDown()

    def _getTargetClass(self):
        from ..site import Site
        return Site

    def _makeOne(self):
        return self._getTargetClass()()

    def test_verify_constructor(self):
        catalog = testing.DummyResource()
        catalog.add = catalog.__setitem__
        registry = self.config.registry
        registry.settings['substanced.secret'] = 's33kr1t'
        registry.settings['substanced.initial_password'] = 's33kr1t'
        registry.settings['substanced.initial_login'] = 'admin@example.com'
        self.config.include('substanced')
        self.config.scan('schoolpack')
        self.config.commit()
        site = self._makeOne()
        # Simulate substanced's factory dance
        site.after_create(site, registry)
        site.after_creation(site, registry)
        self.failUnless('essays' in site)


class DummyContentRegistry(object):

    def create(self, *arg, **kw):
        from substanced.folder import Folder
        return Folder()
