# NimbleServerThread.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import asyncore

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.NimbleServer import NimbleServer
from nimble.connection.thread.NimbleThread import NimbleThread

#___________________________________________________________________________________________________ NimbleServerThread
class NimbleServerThread(NimbleThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ACTIVATING    = False
    _SERVER_THREAD = None

    _ACTIVE_MESSAGE = 'Nimble server is now active'

#___________________________________________________________________________________________________ __init__
    def __init__(self, router =None, **kwargs):
        self.__class__._ACTIVATING = True
        NimbleThread.__init__(self, **kwargs)
        self._server = None
        self._router = router

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ stopServer
    def stopServer(self):
        return self._server.close()

#___________________________________________________________________________________________________ isActivating
    @classmethod
    def isActivating(cls):
        return cls._ACTIVATING

#___________________________________________________________________________________________________ isRunning
    @classmethod
    def isRunning(cls):
        return cls._SERVER_THREAD is not None

#___________________________________________________________________________________________________ closeServer
    @classmethod
    def closeServer(cls):
        if not cls._SERVER_THREAD:
            return False

        cls._SERVER_THREAD.stopServer()
        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        self._server = NimbleServer(router=self._router)
        self.__class__._SERVER_THREAD = self
        self.__class__._ACTIVATING    = False

        NimbleEnvironment.log(NimbleServerThread._ACTIVE_MESSAGE)
        asyncore.loop()
