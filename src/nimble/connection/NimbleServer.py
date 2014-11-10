# NimbleServer.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import asyncore
import socket

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.router.NimbleRouter import NimbleRouter

#AS NEEDED: from nimble.connection.router.MayaRouter import MayaRouter

#___________________________________________________________________________________________________ NimbleServer
class NimbleServer(asyncore.dispatcher):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, router =None):
        asyncore.dispatcher.__init__(self)

        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind(('localhost', NimbleEnvironment.getServerPort()))
            self.listen(5)
        except Exception as err:
            NimbleEnvironment.logError(
                '[ERROR | NIMBLE SERVER] Failed to establish server connection', err)
            raise

        if router is None:
            if NimbleEnvironment.inMaya():
                from nimble.connection.router.MayaRouter import MayaRouter
                self._router = MayaRouter
            else:
                self._router = NimbleRouter
        else:
            self._router = router

#___________________________________________________________________________________________________ handle_accept
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            self._router(sock)

#___________________________________________________________________________________________________ handle_close
    def handle_close(self):
        self.close()

#___________________________________________________________________________________________________ handle_connect
    def handle_connect(self):
        pass
