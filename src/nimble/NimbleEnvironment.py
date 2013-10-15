# NimbleEnvironment.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

import sys
import os
import re
import threading

from pyaid.decorators.ClassGetter import ClassGetter

#___________________________________________________________________________________________________ NimbleEnvironment
class NimbleEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    SOCKET_CHUNK_SIZE      = 8192
    TERMINATION_IDENTIFIER = '#@!NIMBLE_MSG_ENDS!@#'
    REMOTE_RESULT_KEY      = '__nimbleRemoteResponse__'
    REMOTE_KWARGS_KEY      = '__nimbleRemoteKwargs__'

    _inMaya       = None
    _mayaPort     = 7800
    _externalPort = 7801

    _logLevel     = 0
    _mayaUtils    = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: SOCKET_RESPONSE_CHUNK_SIZE
    @ClassGetter
    def SOCKET_RESPONSE_CHUNK_SIZE(cls):
        return 200 if cls.isWindows else cls.SOCKET_CHUNK_SIZE

#___________________________________________________________________________________________________ GS: isWindows
    @ClassGetter
    def isWindows(cls):
        return sys.platform.startswith('win')

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ inMaya
    @classmethod
    def inMaya(cls, override =None):
        if override is not None:
            cls._inMaya = override

        if cls._inMaya is not None:
            return cls._inMaya

        if os.name == 'posix':
            pattern = re.compile('/(M|m)aya20[0-9]*/Maya.app')
        else:
            pattern = re.compile('[\\/]+(M|m)aya20[0-9]*[\\/]+Python')
        if pattern.search(sys.prefix):
            try:
                from maya import utils as mu
                cls._mayaUtils = mu
                cls._inMaya = True
            except Exception, err:
                cls._inMaya = False
            return cls._inMaya

        return cls._inMaya

#___________________________________________________________________________________________________ log
    @classmethod
    def log(cls, message):
        if cls.inMaya() and not threading.currentThread().name.lower() == 'mainthread':
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
