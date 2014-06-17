# MayaNodeUtils.py
# (C)2014
# Scott Ernst

from nimble import cmds

#___________________________________________________________________________________________________ MayaNodeUtils
class MayaNodeUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ getNodeTypes
    @classmethod
    def getNodeTypes(cls, nodeName):
        return cmds.nodeType(nodeName, inherited=True)

#___________________________________________________________________________________________________ isShapeNode
    @classmethod
    def isShapeNode(cls, nodeName):
        return 'shape' in cls.getNodeTypes(nodeName)

#___________________________________________________________________________________________________ isTransformNode
    @classmethod
    def isTransformNode(cls, nodeName):
        return 'transform' in cls.getNodeTypes(nodeName)
