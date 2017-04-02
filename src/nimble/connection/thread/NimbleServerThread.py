# NimbleServerThread.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import \
    print_function, absolute_import, \
    unicode_literals, division

import asyncore

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.NimbleServer import NimbleServer
from nimble.connection.thread.NimbleThread import NimbleThread


class NimbleServerThread(NimbleThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ACTIVATING    = False
    _SERVER_THREAD = None

    _ACTIVE_MESSAGE = 'Nimble server is now active'


    def __init__(self, router =None, **kwargs):
        self._ACTIVATING = True
        NimbleThread.__init__(self, **kwargs)
        self._server = None
        self._router = router

#===================================================================================================
#                                                                                     P U B L I C


    def stopServer(self):
        return self._server.close()


    @classmethod
    def isActivating(cls):
        return cls._ACTIVATING


    @classmethod
    def isRunning(cls):
        return cls._SERVER_THREAD is not None


    @classmethod
    def closeServer(cls):
        if not cls._SERVER_THREAD:
            return False

        cls._SERVER_THREAD.stopServer()
        cls._SERVER_THREAD = None
        return True

#===================================================================================================
#                                                                               P R O T E C T E D


    def _runImpl(self):
        self._server = NimbleServer(router=self._router)
        self._SERVER_THREAD = self
        self._ACTIVATING    = False

        NimbleEnvironment.log(NimbleServerThread._ACTIVE_MESSAGE)
        asyncore.loop()
