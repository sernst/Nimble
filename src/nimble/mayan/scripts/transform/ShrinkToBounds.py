# ShrinkToBounds.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble import cmds
from nimble import NimbleScriptBase

#___________________________________________________________________________________________________ ShrinkToBounds
class ShrinkToBounds(NimbleScriptBase):
    """ Scales each of the selected transform objects in the scene proportionally so that they fit
        within the specified spatial extents along the three spatial axes.

        --- ARGS ---
        [x =None]: The maximum bounding length in the x direction. When None this direction is
            ignored when calculating the scale.
        [y =None]: The maximum bounding length in the y direction. When None this direction is
            ignored when calculating the scale.
        [z =None]: The maximum bounding length in the z direction. When None this direction is
            ignored when calculating the scale.
        [grow =False]: When True, that object will increase its scale to the maximum allowed
            within the bounds. When False, the object will never grow in size; it will remain its
            current size if it is smaller than the specified bounds.

        --- RETURNS ---
        [changes =None]: A dictionary containing the applied relative scales for each object that
            was modified. If no changes were made this property is not returned, which happens if
            nothing was selected, no bounds were specified, or all items already match the
            specified bounds. """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of ShrinkToBounds."""
        NimbleScriptBase.__init__(self)
        self.grow = False
        self.x = None
        self.y = None
        self.z = None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""
        self.x = self.fetch('x', None)
        self.y = self.fetch('y', None)
        self.z = self.fetch('z', None)
        self.grow = self.fetch('grow', False)

        if self.x is None and self.y is None and self.z is None:
            return

        selection = cmds.ls(selection=True, type='transform')
        if not selection:
            return

        out = dict()
        for item in selection:
            scale = self._scaleItem(item)
            if scale is not None:
                out[item] = scale

        if len(list(out.keys())) > 0:
            self.put('changes', out)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _scaleItem
    def _scaleItem(self, item):

        bbox = cmds.exactWorldBoundingBox(item)
        currentX = bbox[3] - bbox[0]
        currentY = bbox[4] - bbox[1]
        currentZ = bbox[5] - bbox[2]

        scale = float('inf')
        if self.x is not None:
            scale = min(scale, float(self.x)/float(currentX))
        if self.y is not None:
            scale = min(scale, float(self.y)/float(currentY))
        if self.z is not None:
            scale = min(scale, float(self.z)/float(currentZ))

        if not self.grow:
            scale = min(scale, 1.0)

        if scale == 1.0:
            return None

        cmds.scale(scale, scale, scale, item, relative=True)
        return scale
