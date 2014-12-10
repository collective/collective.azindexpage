# -*- coding: utf-8 -*-

from collective.azindexpage import logger

def uninstall(portal, reinstall=False):
    if not reinstall:
        # Don't want to delete catalog index
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.azindexpage:uninstall')
        logger.info("Uninstall done")
