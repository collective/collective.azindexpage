import logging

def setupVarious(context):
    marker = 'collective.azindexpage.marker.txt'
    if context.readDataFile(marker) is None:
        # Not your add-on
        return
    logger = logging.getLogger('collective.azindexpage')
    portal = context.getSite()
    catalog = portal.portal_catalog
    logger.info('Reindexin AXIndex; this can take a while')
    catalog.reindexIndex('AZIndex', portal.REQUEST)
    logger.info('Done')
