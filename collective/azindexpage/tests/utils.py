

class FakeAcquisition(object):
    def __init__(self):
        self.aq_explicit = None


class FakeContext(object):

    def __init__(self):
        self.id = "myid"
        self.title = "a title"
        self.description = "a description"
        self.creators = ["myself"]
        self.date = "a date"
        self.aq_inner = FakeAcquisition()
        self.aq_inner.aq_explicit = self
        self._modified = "modified date"

    def getId(self):
        return self.id

    def Title(self):
        return self.title

    def Creators(self):
        return self.creators

    def Description(self):
        return self.description

    def Date(self):
        return self.date

    def modified(self):
        return self._modified

    def getPhysicalPath(self):
        return ('/', 'a', 'not', 'existing', 'path')

    def getFolderContents(self, filter=None):
        catalog = FakeCatalog()
        return catalog.searchResults()

    def absolute_url(self):
        return "http://nohost.com/" + self.id

    def getRemoteUrl(self):  # fake Link
        return self.remoteUrl


class FakeBrain(object):
    def __init__(self):
        self.Title = ""
        self.Description = ""
        self.getId = ""
        self.portal_type = ""

    def getURL(self):
        return "http://fakebrain.com"

    def getObject(self):
        ob = FakeContext()
        ob.title = self.Title

        return ob


class FakeCatalog(object):
    def searchResults(self, **query):
        azindex = query.get('AZIndex', None)
        if azindex is not None:
            if azindex == 'fr-mot-cle1':
                brain1 = FakeBrain()
                brain1.Title = "Un super article"
                brain2 = FakeBrain()
                brain2.Title = "Un autre article"
            if azindex == 'fr-mot-cle2':
                brain1 = FakeBrain()
                brain1.Title = "Un second article"
                brain2 = FakeBrain()
                brain2.Title = "Un autre article"
        return [brain1, brain2]

    __call__ = searchResults

    def modified(self):
        return '654654654654'

    def uniqueValuesFor(self, index):
        if index == 'AZIndex':
            return ['fr-mot-cle1', 'fr-mot-cle2',
                    'en-keyword1', 'en-keyword2']
