# NimbleEnvironment.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

#___________________________________________________________________________________________________ NimbleEnvironment
class NimbleEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _inMaya       = None
    _mayaPort     = 8120
    _externalPort = 8121
    _logLevel     = 0
    _mayaUtils    = None

#___________________________________________________________________________________________________ inMaya
    @classmethod
    def inMaya(cls, override =None):
        if override is not None:
            cls._inMaya = override

        if cls._inMaya is not None:
            return cls._inMaya

        try:
            import maya.utils as mu
            cls._mayaUtils = mu
            cls._inMaya    = True
        except Exception, err:
            cls._inMaya = False

        return cls._inMaya

#___________________________________________________________________________________________________ log
    @classmethod
    def log(cls, message):
        if cls.inMaya():
            cls._mayaUtils.executeInMainThreadWithResult(cls._logMessage, message)
        else:
            cls._logMessage(message)

#___________________________________________________________________________________________________ getServerPort
    @classmethod
    def getServerLogLevel(cls):
        return cls._logLevel

#___________________________________________________________________________________________________ getServerPort
    @classmethod
    def setServerLogLevel(cls, level =0):
        cls._logLevel = level
        return cls._logLevel

#___________________________________________________________________________________________________ getServerPort
    @classmethod
    def getServerPort(cls, inMaya =None):
        return cls._mayaPort if cls.inMaya(override=inMaya) else cls._externalPort

#___________________________________________________________________________________________________ getConnectionPort
    @classmethod
    def getConnectionPort(cls, inMaya =None):
        return cls._externalPort if cls.inMaya(override=inMaya) else cls._mayaPort

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _logMessage
    @classmethod
    def _logMessage(cls, message):
        print message
