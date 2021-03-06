# MayaCommandLink.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import functools

from nimble.NimbleEnvironment import NimbleEnvironment

try:
    # noinspection PyUnresolvedReferences
    import maya.cmds as mc
except Exception:
    maya = None


class MayaCommandLink(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, connection):
        self._connection = connection
        self._commands   = None

        if NimbleEnvironment.inMaya():
            self._commands = mc

#===================================================================================================
#                                                                                     P U B L I C


    def hasAttr(self, attribute):
        parts = attribute.split('.')
        return self.attributeQuery(parts[-1], node=parts[0], exists=True)

#===================================================================================================
#                                                                               I N T R I N S I C


    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError

        if self._commands:
            return getattr(self._commands, item)

        return functools.partial(self._connection.maya, item)
