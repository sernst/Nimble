# NimbleEnvironment.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import sys
import os
import re
import threading

from pyaid.debug.Logger import Logger
from pyaid.decorators.ClassGetter import ClassGetter

from nimble import execution


class NimbleEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    # Default flags sent with client requests to nimble server
    CONNECTION_FLAGS        = 0x00000000

    # When true NimbleRemoteScripts are run in the remote environment by default instead of
    # within Maya. Makes it possible to debug without reloading Maya's Python interpreter for
    # each change. Disable when running in production.
    TEST_REMOTE_MODE        = False

    # Enables gzip compression of the communication to and/or from the nimble server
    ENABLE_COMPRESSION      = False

    # Size of a single chunk of data sent over the socket during communication. Larger messages
    # are broken into multiple chunks of sizes less than or equal to this length
    SOCKET_CHUNK_SIZE       = 8192

    # Number of times socket calls should be attempted before returning in failure
    REMOTE_RETRY_COUNT      = 3

    # Termination string used to identify the end of a nimble message
    TERMINATION_IDENTIFIER  = '#@!NIMBLE_MSG_ENDS!@#'

    # Dictionary key in remote script file's globals() that contain the payload to be returned
    # to the remote Nimble environment once script execution is complete
    REMOTE_RESULT_KEY       = '__nimbleRemoteResponse__'

    # Dictionary key in remote script file's globals() that contain the arguments send by the
    # remote Nimble environment when the script file action is requested
    REMOTE_KWARGS_KEY       = '__nimbleRemoteKwargs__'

    # Error key within the REMOTE_RESULT dictionary in remote scripts that contains an error
    # message for the remote execution. When this key is set the NimbleResultData is set to failure
    # and the error message included in the result
    REMOTE_RESULT_ERROR_KEY = '__nimbleRemoteError__'
    REMOTE_RESULT_WARNING_KEY = '__nimbleRemoteWarning__'

    logger = Logger('nimble', printOut=True)

    _inMaya             = None
    _mayaPort           = 7800
    _externalPort       = 7801

    _logLevel           = 0
    _mayaUtils          = None
    _connectionLifetime = 10

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: CONNECTION_LIFETIME
    @ClassGetter
    def CONNECTION_LIFETIME(cls):
        return cls._connectionLifetime

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
                # noinspection PyUnresolvedReferences
                from maya import utils as mu
                cls._mayaUtils = mu
                cls._inMaya = True
            except Exception as err:
                cls._inMaya = False
            return cls._inMaya

        return cls._inMaya

#___________________________________________________________________________________________________ logError
    @classmethod
    def logError(cls, *args, **kwargs):
        isInMaya = cls.inMaya() and cls._mayaUtils is not None
        if isInMaya and not threading.currentThread().name.lower() == 'mainthread':
            execution.executeWithResult(cls._logError, *args, **kwargs)
        else:
            cls.logger.writeError(*args, **kwargs)

#___________________________________________________________________________________________________ log
    @classmethod
    def log(cls, message):
        isInMaya = cls.inMaya() and cls._mayaUtils is not None
        if isInMaya and not threading.currentThread().name.lower() == 'mainthread':
            execution.executeWithResult(cls._logMessage, message)
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
    def _logMessage(cls, *args, **kwargs):
        cls.logger.write(*args, **kwargs)

#___________________________________________________________________________________________________ _logError
    @classmethod
    def _logError(cls, *args, **kwargs):
        cls.logger.writeError(*args, **kwargs)
