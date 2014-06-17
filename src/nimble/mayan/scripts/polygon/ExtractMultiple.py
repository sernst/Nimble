# ExtractMultiple.py
# (C)2014
# Scott Ernst

from nimble import cmds
from nimble import NimbleScriptBase

#___________________________________________________________________________________________________ ExtractMultiple
from nimble.mayan.MayaNodeUtils import MayaNodeUtils


class ExtractMultiple(NimbleScriptBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of ExtractMultiple."""
        NimbleScriptBase.__init__(self)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""

        #-------------------------------------------------------------------------------------------
        # GET SELECTED OBJECTS
        #       Get a list of select objects. If no objects are selected then return an error.
        #       Because objects are list based on components, shape nodes are generally returned
        #       instead of transform nodes. In those cases the transform node must be found from
        #       the shape node name
        objectSelection = cmds.ls(selection=True, objectsOnly=True)
        if not objectSelection:
            self.putErrorResult(u'Nothing selected')
            return

        targets = dict()
        for obj in objectSelection:

            # Check for shape nodes, and get transform node name if a shape is found
            nodeTypes = cmds.nodeType(obj, inherited=True)
            if u'shape' in nodeTypes:
                obj = obj.rsplit(u'|', 1)[0]

            targets[obj] = []

        #-------------------------------------------------------------------------------------------
        # SORT SELECTED FACES
        #       Use a component selection to get the selected faces and add them to the target
        #       list for their object.
        for comp in cmds.ls(selection=True, flatten=True):
            parts = comp.split(u'.')
            if len(parts) < 2 or parts[0] not in targets:
                continue

            targets[parts[0]].append(int(parts[1].lstrip(u'f[').rstrip(u']')))

        #-------------------------------------------------------------------------------------------
        # EXTRACT & SEPARATE
        #       For each object in the targets list extract the selected faces by chipping them off
        #       and then separating the mesh into the separated pieces.
        results = dict()
        selects = []
        for obj,faces in targets.iteritems():
            if not faces:
                continue

            faces.sort()
            comps = []
            for f in faces:
                comps.append(u'%s.f[%s]' % (obj, f))

            cmds.polyChipOff(*comps, duplicate=False, keepFacesTogether=True)
            separateOut = cmds.polySeparate(obj)
            out = []
            for node in separateOut:
                if MayaNodeUtils.isTransformNode(node):
                    out.append(node)
                    selects.append(node)

            results[obj] = out

        cmds.select(*selects, replace=True)
        self.put('extracts', results)

