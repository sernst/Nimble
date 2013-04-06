# NimbleConnectionWrapper.py
# (C)2013 http://www.ThreeAddOne.com
# Scott Ernst

from nimble.connection.NimbleConnection import NimbleConnection
from nimble.NimbleEnvironment import NimbleEnvironment

#___________________________________________________________________________________________________ NimbleConnectionWrapper
class NimbleConnectionWrapper(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of NimbleConnectionWrapper."""
        self._connection = None

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
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __getattr__
    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError

        if self._connection is None:
            self._connection = self.getNimbleConnection()

        return getattr(self._connection.mayaCommands, item, None)

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
