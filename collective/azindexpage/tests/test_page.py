import unittest2 as unittest
from collective.azindexpage.tests import base
from collective.azindexpage.tests import utils


class UnitTestAZIndexPage(base.UnitTestCase):

    def setUp(self):
        from collective.azindexpage.browser import page
        super(UnitTestAZIndexPage, self).setUp()
        self.context = utils.FakeContext()
        self.view = page.AZIndexPage(self.context, {})
        self.view._language = 'fr'
        self.view._catalog = utils.FakeCatalog()

    def test_update(self):
        self.assertTrue(not self.view.updated)
        self.assertTrue(not self.view._words)
        self.assertTrue(not self.view._azwords)
        self.view.update()
        self.assertTrue(self.view.updated)
        self.assertTrue(len(self.view._words) == 2)
        self.assertIn('mot-cle1', self.view._words)
        self.assertIn('mot-cle2', self.view._words)
        self.assertIn('m', self.view._azwords)
        self.assertTrue(len(self.view._azwords) == 1)
        self.assertTrue(len(self.view._azwords.values()[0]) == 2)

        #remove cache and change language to an empty one
        self.view.updated = False
        self.view._language = 'es'
        self.view._words = []
        self.view._azwords = {}
        self.view.update()
        self.assertTrue(self.view.updated)
        self.assertTrue(len(self.view._words) == 0)
        self.assertTrue(len(self.view._azwords) == 0)

        self.view.updated = False
        self.view._language = 'en'
        self.view._words = []
        self.view._azwords = {}
        self.view.update()
        self.assertTrue(self.view.updated)
        self.assertTrue(len(self.view._words) == 2)
        self.assertIn('keyword1', self.view._words)
        self.assertIn('keyword2', self.view._words)
        self.assertIn('k', self.view._azwords)
        self.assertTrue(len(self.view._azwords) == 1)

    def test_get_pages_for(self):
        self.view.update()
        pages = self.view.get_pages_for('mot-cle1')
        self.assertTrue(len(pages) == 2)
        titles = [page['title'] for page in pages]
        self.assertIn("Un super article", titles)
        self.assertIn("Un autre article", titles)

        pages = self.view.get_pages_for('mot-cle2')
        self.assertTrue(len(pages) == 2)
        titles = [page['title'] for page in pages]
        self.assertIn("Un second article", titles)
        self.assertIn("Un autre article", titles)


class IntegrationTestAZIndexPage(base.IntegrationTestCase):
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
