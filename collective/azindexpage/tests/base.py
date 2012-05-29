import transaction
import unittest2 as unittest
import tempfile
from subprocess import call
from pyquery import PyQuery as pq
from plone.app import testing as ptesting
from collective.azindexpage import testing
from plone.testing.z2 import Browser


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        pass


class IntegrationTestCase(unittest.TestCase):

    layer = testing.INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']
        ptesting.setRoles(self.portal, ptesting.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.portal['test-folder'].setTitle('Test folder')
        self.portal['test-folder'].reindexObject()
        ptesting.setRoles(self.portal, ptesting.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


class FunctionalTestCase(IntegrationTestCase):

    layer = testing.FUNCTIONAL

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        # Commit so that the test browser sees these changes
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        user = ptesting.TEST_USER_NAME
        password = ptesting.TEST_USER_PASSWORD
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()
        self.browser.getLink('Home').click()

    def openInBrowser(self):
        fd, fn = tempfile.mkstemp(suffix=".html", prefix="testbrowser-")
        f = open(fn, 'w')
        f.write(self.browser.contents)
        f.close()
        call(["open", fn])

    def setRole(self, role):
        ptesting.setRoles(self.portal, ptesting.TEST_USER_ID, [role])
        transaction.commit()

    def assertElement(self, selector, length=None):
        wrapper = pq(self.browser.contents)
        element = wrapper(selector)
        self.assertTrue(element, "%s not in page" % selector)
        if length is not None:
            msg = "There are %s elements on the pattern %s" % (len(element),
                                                               selector)
            self.assertEqual(len(element), length, msg)
