import unittest2 as unittest
from collective.azindexpage.tests import base


class TestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_catalog(self):
        catalog = self.portal.portal_catalog
        self.assertTrue('AZIndex' in catalog.indexes())

    def test_dependencies(self):
        dep = 'archetypes.linguakeywordwidget'
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled(dep))

    def test_resources(self):
        cssid = '++resource++azindexpage.css'
        cssregistry = self.portal.portal_css
        resource = cssregistry.getResource(cssid)
        self.assertTrue(resource.getEnabled())

        jsid = '++resource++azindexpage.js'
        jsregistry = self.portal.portal_javascripts
        resource = jsregistry.getResource(jsid)
        self.assertTrue(resource.getEnabled())

    def test_view_methods(self):
        views = self.portal.portal_types.getTypeInfo('Document').view_methods
        self.assertTrue("azindexpage" in views)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
