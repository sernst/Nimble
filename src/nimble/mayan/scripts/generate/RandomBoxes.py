# RandomBoxes.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import math

from pyaid.debug.Logger import Logger
import elixir

import nimble
from nimble import cmds
from nimble import NimbleScriptBase
from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.mayan.TransformUtils import TransformUtils

#___________________________________________________________________________________________________ RandomBoxes
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
        self._padding = 0.0
        self._meshPointNode = None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""

        self.saveSelection()

        count = self.fetch('count', 1000)
        self._size = self.fetch('size', 0.1)
        self._padding = self.fetch('padding', 0.0)

        transforms = cmds.ls(selection=True, type='transform')
        if not transforms:
            self._cleanup()
            self.putErrorResult(u'ERROR: No transforms selected')
            return

        shapes = []
        totalVolume = 0.0
        shapeCount = 0
        for transform in transforms:
            shapeNames = cmds.listRelatives(transforms, shapes=True)
            if not shapeNames:
                continue

            for shape in shapeNames:
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
                    shapeCount += 1
                except Exception as err:
                    self._cleanup()
                    NimbleEnvironment.logError(u'ERROR: Shape processing', err)

                    self.putErrorResult(
                        u'ERROR: Unable to process selection item %s -> %s' % (transform, shape) )
                    return

        if shapeCount == 0:
            self._cleanup()
            self.putErrorResult(u'ERROR: No polygon transforms found in selection')
            return

        try:
            for shape in shapes:
                if not self._createMeshPointNode(shape):
                    self._cleanup()
                    print(u'ERROR: Creation failure')
                    self.putErrorResult(u'ERROR: Unable to create point test node')

                shape['weight'] /= totalVolume
                shapeCount = int(round(float(count)*shape['weight']))
                for i in range(shapeCount):
                    self._create(shape)

                self._removeMeshPointNode()
        except Exception as err:
            self._cleanup()
            print(Logger.createErrorMessage(u'ERROR: Creation failure', err))
            self.putErrorResult(u'ERROR: Unable to create random box')
            return

        self._cleanup()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _create
    def _create(self, shapeData):
        point = None
        count = 0
        while True:
            count += 1
            if count > 10000:
                return False

            point = shapeData['box'].getRandomPointInside(padding=self._padding)

            if not cmds.elixirGeneral_PointInsideMesh(mesh=shapeData['name'], point=point):
                continue

            if self._padding > 0:
                cmds.setAttr(self._meshPointNode + '.inPosition', *point, type='double3')
                closestPoint = cmds.getAttr(self._meshPointNode + '.result.position')[0]

                dx = (closestPoint[0] - point[0])
                dy = (closestPoint[1] - point[1])
                dz = (closestPoint[2] - point[2])
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)

                if dist < self._padding:
                    continue
            break

        cube = cmds.polyCube(width=self._size, height=self._size, depth=self._size)
        cmds.move(point[0], point[1], point[2], cube[0], absolute=True)
        return True

#___________________________________________________________________________________________________ _cleanup
    def _cleanup(self):
        self._removeMeshPointNode()

        self.restoreSelection()

#___________________________________________________________________________________________________ _createMeshPointNode
    def _createMeshPointNode(self, shapeData):
        self._removeMeshPointNode()

        try:
            node = cmds.createNode('closestPointOnMesh', skipSelect=True)
            self._meshPointNode = node
        except Exception as err:
            print(Logger.createErrorMessage(u'ERROR: Unable to create mesh point node', err))
            self._removeMeshPointNode()
            return False

        try:
            cmds.connectAttr(shapeData['name'] + '.message', node + '.inMesh', force=True)
        except Exception as err:
            print(Logger.createErrorMessage(u'ERROR: Unable to connect mesh point node to shape', err))
            self._removeMeshPointNode()
            return False

        return True

#___________________________________________________________________________________________________ _removeMeshPointNode
    def _removeMeshPointNode(self):
        if self._meshPointNode is None:
            return

        try:
            cmds.delete(self._meshPointNode)
        except Exception:
            pass
        self._meshPointNode = None
