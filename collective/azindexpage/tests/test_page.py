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
        self.assertEqual(len(self.view._words), 2)
        self.assertIn('mot-cle1', self.view._words)
        self.assertIn('mot-cle2', self.view._words)
        self.assertIn('m', self.view._azwords)
        self.assertEqual(len(self.view._azwords), 1)
        self.assertEqual(len(self.view._azwords.values()[0]), 2)

        #remove cache and change language to an empty one
        self.view.updated = False
        self.view._language = 'es'
        self.view._words = []
        self.view._azwords = {}
        self.view.update()
        self.assertTrue(self.view.updated)
        self.assertEqual(len(self.view._words), 0)
        self.assertEqual(len(self.view._azwords), 0)

        self.view.updated = False
        self.view._language = 'en'
        self.view._words = []
        self.view._azwords = {}
        self.view.update()
        self.assertTrue(self.view.updated)
        self.assertEqual(len(self.view._words), 2)
        self.assertIn('keyword1', self.view._words)
        self.assertIn('keyword2', self.view._words)
        self.assertIn('k', self.view._azwords)
        self.assertEqual(len(self.view._azwords), 1)

    def test_get_pages_for(self):
        self.view.update()
        pages = self.view.get_pages_for('mot-cle1')
        self.assertEqual(len(pages), 2)
        titles = [page['title'] for page in pages]
        self.assertIn("Un super article", titles)
        self.assertIn("Un autre article", titles)

        pages = self.view.get_pages_for('mot-cle2')
        self.assertEqual(len(pages), 2)
        titles = [page['title'] for page in pages]
        self.assertIn("Un second article", titles)
        self.assertIn("Un autre article", titles)

    def test_get_letters(self):
        letters = self.view.get_letters()
        self.assertEqual(len(letters), 26)
        self.assertEqual(letters[0], 'a')
        self.assertEqual(letters[25], 'z')


class IntegrationTestAZIndexPage(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def setAZIndex(self, content, keywords):
        mutator = content.getField('azindex').getMutator(content)
        mutator(keywords)
        content.reindexObject()

    def setUp(self):
        from collective.azindexpage.browser import page
        super(IntegrationTestAZIndexPage, self).setUp()
        self.view = page.AZIndexPage(self.portal, self.portal.REQUEST)
        self.setAZIndex(self.folder, ['en-keyword1'])
        self.view.update()

    def test_update(self):
        self.assertTrue(self.view.updated)
        self.assertEqual(len(self.view._words), 1)
        self.assertIn('keyword1', self.view._words)
        self.assertIn('k', self.view._azwords)
        self.assertEqual(len(self.view._azwords), 1)

    def test_get_pages_for(self):
        pages = self.view.get_pages_for('keyword1')
        self.assertEqual(len(pages), 1)
        page = pages[0]
        self.assertIn("URL", page)
        self.assertIn("description", page)
        self.assertIn("title", page)
        self.assertEqual(page["title"], "Test folder")
        self.assertEqual(page["URL"], self.folder.absolute_url())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
