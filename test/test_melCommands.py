# test_melCommands.py
# (C)2014
# Scott Ernst

""" A unit test for the Nimble bridge to test the execution of mel commands. """

import nimble
from nimble import cmds

cubeNode = cmds.polyCube(width=2, height=2, depth=4)
print 'CREATED:', cubeNode
cubeShape = cmds.listRelatives(cubeNode[0], shapes=True)
print 'SHAPE:', cubeShape

cmds.select(cubeShape[0], replace=True)
result = nimble.executeMelCommand('computePolysetVolume', nimbleResult=True)
print result.echo(verbose=True, pretty=True)
