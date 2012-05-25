

def setupVarious(context):
    marker = 'collective.azindexpage.marker.txt'
    if context.readDataFile(marker) is None:
        # Not your add-on
        return
    portal = context.getSite()
    catalog = portal.portal_catalog
    catalog.reindexIndex('AZIndex', portal.REQUEST)
