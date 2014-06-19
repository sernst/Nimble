# RandomBoxes.py
# (C)2014
# Scott Ernst

from pyaid.debug.Logger import Logger

import nimble
from nimble import cmds
from nimble import NimbleScriptBase

import elixir

#___________________________________________________________________________________________________ RandomBoxes
from nimble.mayan.TransformUtils import TransformUtils


class RandomBoxes(NimbleScriptBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of RandomBoxes."""
        NimbleScriptBase.__init__(self)

        # Load the elixir general plugin if not already loaded
        elixir.loadGeneralPlugin()

        self._size = 1.0

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""

        self.saveSelection()

        count = self.fetch('count', 1000)
        self._size = self.fetch('size', 0.1)

        transforms = cmds.ls(selection=True, type='transform')
        if not transforms:
            self.putErrorResult('ERROR: No transforms selected')
            return

        shapes = []
        totalVolume = 0.0
        for transform in transforms:
            for shape in cmds.listRelatives(transforms, shapes=True):
                try:
                    box = TransformUtils.getBoundingBox(shape)
                    cmds.select(shape, replace=True)
                    shapeVolume = nimble.executeMelCommand('computePolysetVolume')
                    totalVolume += shapeVolume
                    shapes.append(dict(
                        transform=transform,
                        name=shape,
                        box=box,
                        weight=float(shapeVolume)) )
                except Exception, err:
                    print Logger.createErrorMessage(u'ERROR: Shape processing', err)

                    self.putErrorResult(
                        u'ERROR: Unable to process selection item %s -> %s' % (transform, shape) )
                    return

        try:
            for shape in shapes:
                shape['weight'] /= totalVolume
                shapeCount = int(round(float(count)*shape['weight']))
                for i in range(shapeCount):
                    self._create(shape)
        except Exception, err:
            print Logger.createErrorMessage(u'ERROR: Creation failure', err)
            self.putErrorResult(u'ERROR: Unable to create random box')
            return

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _create
    def _create(self, shapeData):
        point = shapeData['box'].getRandomPointInside()
        while not cmds.elixirGeneral_PointInsideMesh(mesh=shapeData['name'], point=point):
            point = shapeData['box'].getRandomPointInside()

        cube = cmds.polyCube(width=self._size, height=self._size, depth=self._size)
        cmds.move(point[0], point[1], point[2], cube[0], absolute=True)
