import transaction
import unittest2 as unittest
from plone.app import testing as ptesting
from collective.azindexpage import testing


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
        ptesting.setRoles(self.portal, ptesting.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


class FunctionalTestCase(IntegrationTestCase):

    layer = testing.FUNCTIONAL

    def setUp(self):
        #we must commit the transaction
        transaction.commit()
