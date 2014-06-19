# TransformUtils.py
# (C)2014
# Scott Ernst

from nimble import cmds
from nimble.utils.data.BoundingBox3D import BoundingBox3D

#___________________________________________________________________________________________________ TransformUtils
class TransformUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ getBoundingBox
    @classmethod
    def getBoundingBox(cls, dagPath):
        """ Calculates the world bounding box for the specified dag path and returns a
            BoundingBox3D instance populated with those values. """

        box = BoundingBox3D()
        box.fromExactWorldBoundingBox(cmds.exactWorldBoundingBox(dagPath))
        return box
