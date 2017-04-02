# PolygonUtils.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import re

from nimble import cmds


class PolygonUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TOLERANCE = 0.0001

    _VERTEX_INDEX_RE      = re.compile('\[(?P<v>[0-9:]+)]$')
    _VERTEX_FACE_INDEX_RE = re.compile('\[(?P<v>[0-9:]+)]\[(?P<f>[0-9:]+)]$')


    @classmethod
    def edgeToVertices(cls, transform, edgeIndex):
        return cls._getIndexesFromSelectionList(
            cmds.polyListComponentConversion(
               '%s.e[%s]' % (transform, edgeIndex), fromEdge=True, toVertex=True) )


    @classmethod
    def edgeToFaces(cls, transform, edgeIndex):
        return cls._getIndexesFromSelectionList(
            cmds.polyListComponentConversion(
               '%s.e[%s]' % (transform, edgeIndex), fromEdge=True, toFace=True) )


    @classmethod
    def vertexToFaces(cls, transform, vertexIndex):
        return cls._getIndexesFromSelectionList(
           cmds.polyListComponentConversion(
               '%s.vtx[%s]' % (transform, vertexIndex), fv=True, tvf=True) )


    @classmethod
    def faceToVertexIndices(cls, transform, faceIndex):
        """ This method exists to convert a face to a list of correctly (counter-clockwise) ordered
           vertex indices. """

        vertexFaceSelections = cmds.filterExpand(
           cmds.polyListComponentConversion(
               '%s.f[%s]' % (transform, faceIndex), ff=True, tvf=True),
           sm=70, expand=True)

        vertexIndices = []
        for entry in vertexFaceSelections:
           result = cls._VERTEX_FACE_INDEX_RE.search(entry)
           vertexIndices.append(int(result.groupdict()['v']))
        return vertexIndices


    @classmethod
    def vertexFaceToUVCoordinate(cls, transform, vertexIndex, faceIndex):
        uvIndexes = cls._getIndexesFromSelectionList(
           cmds.polyListComponentConversion(
               '%s.vtxFace[%s][%s]' % (transform, vertexIndex, faceIndex), fvf=True, tuv=True))
        if not uvIndexes:
            return None
        return cmds.getAttr('%s.uv[%s]' % (transform, uvIndexes[0]))[0]


    @classmethod
    def vertexFaceToNormal(cls, transform, vertexIndex, faceIndex):
        return cmds.polyNormalPerVertex(
           '%s.vtxFace[%s][%s]' % (transform, vertexIndex, faceIndex), query=True, xyz=True)


    @classmethod
    def getPositionOfVertex(cls, transform, vertexIndex):
        return cmds.xform('%s.pnts[%s]' % (transform, vertexIndex),
           query=True,
           worldSpace=True,
           translation=True)

#===================================================================================================
#                                                                               P R O T E C T E D


    @classmethod
    def _getIndexesFromSelectionList(cls, selectionList):
        indexes = []

        for entry in selectionList:
           result = cls._VERTEX_INDEX_RE.search(entry)
           values = result.groupdict()['v'].split(':')

           # Start vertex
           v = int(values[0])
           if len(indexes) == 0 or indexes[-1] != v:
               indexes.append(v)

           if len(values) == 1:
               continue

           vend = int(values[1])
           for index in range(v + 1, vend + 1):
               indexes.append(index)

        return indexes

