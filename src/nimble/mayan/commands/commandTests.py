# NimbleConnection.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble import cmds

#___________________________________________________________________________________________________ HelloCommandTest
class HelloCommandTest(object):
    """A class for..."""

#___________________________________________________________________________________________________ __init__
    def __init__(self, width =1, name =None):
        print('CONSTRUCTED: [width: %s], [name: %s]' % (str(width), str(name)))
        self._width = width
        self._name  = name

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ instanceCube
    def instanceCube(self, **kwargs):
        """Doc..."""
        name   = self._name if self._name else 'instanceCube'
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name=name, height=height, width=self._width)
        cmds.move(x, 10, 0, res[0])
        return res

#___________________________________________________________________________________________________ classyCube
    @classmethod
    def classyCube(cls, **kwargs):
        """Doc..."""
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name='classyCube', height=height)
        cmds.move(x, 20, 0, res[0])
        return res

#___________________________________________________________________________________________________ staticCube
    @staticmethod
    def staticCube(**kwargs):
        """Doc..."""
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name='staticCube', height=height)
        cmds.move(x, 30, 0, res[0])
        return res

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, **kwargs):
        name   = self._name if self._name else 'calledCube'
        height = kwargs['height'] if 'height' in kwargs else 2
        x      = kwargs['x'] if 'x' in kwargs else 0
        res    = cmds.polyCube(name=name, height=height, width=self._width)
        cmds.move(x, 40, 0, res[0])
        return res

#===================================================================================================
#                                                                               F U N C T I O N S

#___________________________________________________________________________________________________ functionCube
def functionCube(**kwargs):
    height = kwargs['height'] if 'height' in kwargs else 2
    x      = kwargs['x'] if 'x' in kwargs else 0
    res     = cmds.polyCube(name='functionCube', height=height)
    cmds.move(x, 50, 0, res[0])
    return res

