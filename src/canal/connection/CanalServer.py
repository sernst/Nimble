# CanalServer.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

import asyncore
import socket

from canal.CanalEnvironment import CanalEnvironment
from canal.connection.router.CanalRouter import CanalRouter
#AS NEEDED: from canal.connection.router.MayaRouter import MayaRouter

#___________________________________________________________________________________________________ CanalServer
class CanalServer(asyncore.dispatcher):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, router =None):
        asyncore.dispatcher.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('localhost', CanalEnvironment.getServerPort()))
        self.listen(5)

        if router is None:
            if CanalEnvironment.inMaya():
                from canal.connection.router.MayaRouter import MayaRouter
                self._router = MayaRouter
            else:
                self._router = CanalRouter
        else:
            self._router = router

#___________________________________________________________________________________________________ handle_accept
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            handler = self._router(sock)
