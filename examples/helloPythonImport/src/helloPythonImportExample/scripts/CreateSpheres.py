# CreateSpheres.py
# (C)2014
# Scott Ernst

import math

from nimble import cmds
from nimble import NimbleScriptBase

#___________________________________________________________________________________________________ CreateSpheres
class CreateSpheres(NimbleScriptBase):
    """ A Nimble script example for creating rings of spheres in the scene.

        --- ARGS ---
        [count]:    (integer) (default: 6) The number of spheres that should make of the ring.
        [radius]:   (float) (default: 10) The radius of the ring of spheres.
        [y]:        (float) (default: 0) The y-axis height of the ring of spheres.

        --- RETURNS ---
        ringName:       (string) The name of the group node representing the ring of spheres.
        sphereNames:    (string[]) (default: []) A list of the node names for each sphere in
                                the created ring. """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """ Creates a new instance of CreateSpheres. As a NimbleScriptBase derived class the
            constructor must not take any arguments, as nothing is passed by Nimble when the
            class is used. Instead arguments are assigned to the class later in its life-cycle
            just prior to calling the run command. """
        NimbleScriptBase.__init__(self)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """ This method is where your nimble script should be implemented. Prior to Nimble calling
            this method the class receives the arguments passed through Nimble needed by the
            your method implementation. """

        # Retrieve the arguments passed by Nimble using the fetch method, which includes a default
        # value to assign if the argument was not specified in the Nimble call
        sphereCount = self.fetch('count', 6)
        ringRadius  = self.fetch('radius', 10)
        yOffset     = self.fetch('y', 0)

        # Create the spheres using Maya commands imported through Nimble, which allows this script
        # to be run flexibly both inside and outside of Maya
        sphereNames = []
        for i in range(sphereCount):
            result = cmds.sphere()
            sphereNames.append(result[0])

            # Position the sphere in the ring
            cmds.move(
                ringRadius*math.cos(2.0*math.pi*i/sphereCount),
                0,
                ringRadius*math.sin(2.0*math.pi*i/sphereCount),
                result[0])

        # Place the spheres within a group node to represent the ring and move the group up the
        # y-axis by the value specified by the script arguments
        ringGroupNode = cmds.group(*sphereNames, name='sphereRing1')
        cmds.move(0, yOffset, 0, ringGroupNode)

        # Set the results of the script with the put command for returning to the Nimble calling
        # environment
        self.put('ringName', ringGroupNode)
        self.put('sphereNames', sphereNames)

