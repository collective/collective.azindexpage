from Products.Five.browser import BrowserView
from zope import interface
from zope import component
from Products.CMFCore.utils import getToolByName


class IAZIndexPageHelper(interface.Interface):
    """Helper to build an A-Z index page"""

    def get_az_words():
        """Return a structure with all words
        -> ('a': ('animal', ...), 'b': (), ...)
        """

    def get_words(letter):
        """Returns all indexed words starting by letter"""

    def letters():
        """Returns the a-z letters"""

    def get_pages_for(word):
        """Return full URL to search for items with that words"""


class AZIndexPage(BrowserView):
    """A-Z index page"""
    interface.implements(IAZIndexPageHelper)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._language = None
        self._catalog = None
        self._words = []
        self._azwords = {}
        self.updated = False

    def update(self):

        if self.updated:
            return

        if not self._language:
            cstate = component.getMultiAdapter((self.context, self.request),
                                               name=u'plone_portal_state')
            self._language = cstate.language()

        if not self._catalog:
            self._catalog = getToolByName(self.context, 'portal_catalog')

        if not self._words:

            words = self._catalog.uniqueValuesFor('AZIndex')
            marker = '%s-' % self._language
            len_marker = len(marker)
            for word in words:
                if word.startswith(marker):
                    self._words.append(word[len_marker:])

        if not self._azwords:
            for word in self._words:
                letter = word[0].lower()  # TODO: normalize
                if letter not in self._azwords:
                    self._azwords[letter] = []
                self._azwords[letter].append(word)

        self.updated = True

    def get_words(self, letter):
        if not self.updated:
            self.update()

        return self._azwords.get(letter)

    def get_az_words(self):
        if not self.updated:
            self.update()

        return self._azwords

    def get_letters(self):
        return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def get_pages_for(self, word):
        if not self.updated:
            self.update()

        query = {'AZIndex': '%s-%s' % (self._language, word)}
        brains = self._catalog(**query)
        pages = []

        for brain in brains:
            pages.append({'URL': brain.getURL(),
                'title': brain.Title,
                'description': brain.Description})

        return pages
