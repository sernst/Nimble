# NimbleConnection.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

from nimble import cmds

#___________________________________________________________________________________________________ HelloCommandTest
class HelloCommandTest(object):
    """A class for..."""

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ instanceCube
    def instanceCube(self, *args, **kwargs):
        """Doc..."""
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name='instanceCube', height=height)
        cmds.move(x, 10, 0, res[0])
        return res

#___________________________________________________________________________________________________ classyCube
    @classmethod
    def classyCube(cls, *args, **kwargs):
        """Doc..."""
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name='classyCube', height=height)
        cmds.move(x, 20, 0, res[0])
        return res

#___________________________________________________________________________________________________ staticCube
    @staticmethod
    def staticCube(*args, **kwargs):
        """Doc..."""
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name='staticCube', height=height)
        cmds.move(x, 30, 0, res[0])
        return res

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, *args, **kwargs):
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name='calledCube', height=height)
        cmds.move(x, 40, 0, res[0])
        return res

#===================================================================================================
#                                                                               F U N C T I O N S

#___________________________________________________________________________________________________ functionCube
def functionCube(*args, **kwargs):
    height = kwargs['height'] if 'height' in kwargs else 2
    x      = kwargs['x'] if 'x' in kwargs else 0
    res     = cmds.polyCube(name='functionCube', height=height)
    cmds.move(x, 50, 0, res[0])
    return res

