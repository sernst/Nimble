# NimbleThread.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import threading


class NimbleThread(threading.Thread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self._server = None

#===================================================================================================
#                                                                                     P U B L I C


    def run(self):
        if self.__class__.isRunning():
            return

        return self._runImpl()


    @classmethod
    def isRunning(cls):
        return False

#===================================================================================================
#                                                                               P R O T E C T E D


    def _runImpl(self):
        pass
