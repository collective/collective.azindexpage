from zope.component import adapts
from zope.interface import implements, Interface

from plone.indexer import indexer
from Products.Archetypes import public as atapi
from Products.Archetypes.interfaces import IBaseContent

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, \
    IBrowserLayerAwareExtender

# Your add-on browserlayer
from collective.azindexpage.browser.interfaces import ILayer
from archetypes.linguakeywordwidget.widget import LinguaKeywordWidget

from zope import i18nmessageid
_ = i18nmessageid.MessageFactory('collective.azindexpage')

#Load template translations
_(u"Empty pane")


class ExtensionLinesField(ExtensionField, atapi.LinesField):
    """MultiLingual LinesField"""


class AZIndexExtender(object):
    """This extender just add a new field to all content types
    """

    # This extender will apply to all Archetypes based content
    adapts(IBaseContent)

    # We use both orderable and browser layer aware sensitive properties
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    # Don't do schema extending unless our add-on product is installed on Plone
    layer = ILayer

    fields = [
        ExtensionLinesField("azindex",
            schemata="settings",
            accessor="AZIndex",
            widget=LinguaKeywordWidget(
              label=_(u"A-Z Index page"),
              description=_(u"Select keywords to include this page in index"),
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.

        @param schematas: Dictonary of schemata name -> field lists

        @return: Dictionary of reordered field lists per schemata.
        """

        return schematas

    def getFields(self):
        """
        @return: List of new fields we contribute to content.
        """
        return self.fields


@indexer(Interface)
def AZIndex(obj):
    """Is this the default page in its folder
    """
    if not hasattr(obj, 'getField'):
        return []
    field = obj.getField('azindex')
    if field is None:
        return []
    return field.get(obj)
