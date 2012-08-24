# CanalServerThread.py
# (C)2012 http://www.threeAddOne.com
# Scott Ernst

import asyncore

from canal.CanalEnvironment import CanalEnvironment
from canal.connection.CanalServer import CanalServer
from canal.connection.thread.CanalThread import CanalThread

#___________________________________________________________________________________________________ CanalServerThread
class CanalServerThread(CanalThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ACTIVATING    = False
    _SERVER_THREAD = None

    _ACTIVE_MESSAGE = 'CANAL Server is now active'

#___________________________________________________________________________________________________ __init__
    def __init__(self, router =None, **kwargs):
        self.__class__._ACTIVATING = True
        CanalThread.__init__(self, **kwargs)
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
        self._server = CanalServer(router=self._router)
        self.__class__._SERVER_THREAD = self
        self.__class__._ACTIVATING    = False

        CanalEnvironment.log(CanalServerThread._ACTIVE_MESSAGE)
        asyncore.loop()
