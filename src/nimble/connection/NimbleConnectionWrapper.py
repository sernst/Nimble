# NimbleConnectionWrapper.py
# (C)2013-2014
# Scott Ernst

from nimble.connection.NimbleConnection import NimbleConnection
from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.support.CustomCommandLink import CustomCommandLink
from nimble.connection.support.MayaCommandLink import MayaCommandLink

#___________________________________________________________________________________________________ NimbleConnectionWrapper
class NimbleConnectionWrapper(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    MAYA_COMMANDS  = 'mayaCommands'
    NIMBLE_SCRIPTS = 'nimbleScripts'
    CUSTOM_SCRIPTS = 'customScripts'

#___________________________________________________________________________________________________ __init__
    def __init__(self, wrapperType, **kwargs):
        """Creates a new instance of NimbleConnectionWrapper."""
        self._kwargs = kwargs
        self._connection = None
        self._wrapperType = wrapperType
        self._linker = None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getNimbleConnection
    @classmethod
    def getNimbleConnection(cls, inMaya =None, forceCreate =None):
        NimbleEnvironment.inMaya(override=inMaya)
        try:
            return NimbleConnection.getConnection(forceCreate=forceCreate)
        except Exception, err:
            raise Exception

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getLinker
    def _getLinker(self):
        if self._linker is not None:
            return self._linker

        if self._connection is None:
            self._connection = self.getNimbleConnection()

        if self._wrapperType == self.MAYA_COMMANDS:
            self._linker = MayaCommandLink(connection=self._connection)
        else:
            self._linker = CustomCommandLink(connection=self._connection, **self._kwargs)

        return self._linker

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, *args, **kwargs):
        linker = self._getLinker()

        if self._wrapperType == self.MAYA_COMMANDS:
            return getattr(linker, args[0], None)

        return linker(*args, **kwargs)

#___________________________________________________________________________________________________ __getitem__
    def __getitem__(self, item):
        return self.__call__(item)

#___________________________________________________________________________________________________ __getattr__
    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError

        return getattr(self._getLinker(), item, None)

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
