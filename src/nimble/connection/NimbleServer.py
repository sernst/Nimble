# NimbleServer.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import asyncore
import socket

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.router.NimbleRouter import NimbleRouter

#AS NEEDED: from nimble.connection.router.MayaRouter import MayaRouter


class NimbleServer(asyncore.dispatcher):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, router =None):
        asyncore.dispatcher.__init__(self)

        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind((
                NimbleEnvironment.getServerHost(),
                NimbleEnvironment.getServerPort()
            ))
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


    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            self._router(sock)


    def handle_close(self):
        self.close()


    def handle_connect(self):
        pass
