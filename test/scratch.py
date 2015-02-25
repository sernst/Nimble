from __future__ import print_function, absolute_import, unicode_literals, division

from nimble.connection.NimbleConnection import NimbleConnection

connection = None
try:
    from maya import cmds
except Exception:
    connection = NimbleConnection.getConnection()

# Create a sphere
sphereName, sphereShape = connection.maya('sphere') if connection else cmds.sphere()

# Move the created sphere to x=10
connection.maya('move', 10, 0, 0, sphereName) if connection else cmds.move(10, 0, 0, sphereName)

