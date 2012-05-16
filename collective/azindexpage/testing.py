from plone.testing import z2

from plone.app.testing import *
import collective.azindexpage

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=collective.azindexpage,
                                additional_z2_products=[],
                                gs_profile_id='collective.azindexpage:default',
                                name="collective.azindexpage:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.azindexpage:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.azindexpage:Functional")

