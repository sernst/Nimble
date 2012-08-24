# test_importedCommands.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import nimble
from nimble import CommandImport
from nimble.mayan.commands.commandTests import HelloCommandTest
from nimble.mayan.commands.commandTests import functionCube

#---------------------------------------------------------------------------------------------------
# Locally imported tests

print 'Local static:', HelloCommandTest.staticCube(x=20, height=5)
print 'Local class:', HelloCommandTest.classyCube(x=20, height=5)
print 'Local called:', HelloCommandTest()(x=20, height=5)
print 'Local instance:', HelloCommandTest().instanceCube(x=20, height=5)
print 'Local function:', functionCube(x=20, height=5)

#---------------------------------------------------------------------------------------------------
# Remotely imported tests
conn = nimble.getConnection()

print 'Static result: ', conn.command(
    CommandImport('HelloCommandTest', 'nimble.mayan.commands.commandTests', 'staticCube'),
    x=-20,
    height=5
)

print 'Class result: ', conn.command(
    CommandImport('HelloCommandTest', 'nimble.mayan.commands.commandTests', 'classyCube'),
    x=-20,
    height=5
)

print 'Called result: ', conn.command(
    CommandImport('HelloCommandTest', 'nimble.mayan.commands.commandTests'),
    x=-20,
    height=5
)

print 'Instance result: ', conn.command(
    CommandImport('HelloCommandTest', 'nimble.mayan.commands.commandTests', 'instanceCube'),
    x=-20,
    height=5
)

print 'Function result: ', conn.command(
    CommandImport('functionCube', 'nimble.mayan.commands.commandTests'),
    x=-20,
    height=5
)

print 'Tests complete!'
