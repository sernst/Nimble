# MayaNodeUtils.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble import cmds


class MayaNodeUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    @classmethod
    def getNodeTypes(cls, nodeName):
        return cmds.nodeType(nodeName, inherited=True)


    @classmethod
    def isShapeNode(cls, nodeName):
        return 'shape' in cls.getNodeTypes(nodeName)


    @classmethod
    def isTransformNode(cls, nodeName):
        return 'transform' in cls.getNodeTypes(nodeName)
