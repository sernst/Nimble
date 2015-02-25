# helloNimble.py
# (C)2014
# Scott Ernst

""" Before using this example you must be running Maya with an active Nimble server session. See
    the Nimble ReadMe for more details.

    The most basic and common usage of Nimble is through the commands module, which behaves
    identically to the Maya commands module with the added benefit that it can be run both inside
    Maya and remotely through a Nimble server connection.

    To use the Maya Python commands the import statement at the beginning of your script looks like:

        from maya import cmds

    and then you can call commands, such as:

        cmds.move(1, 0, 0, 'someNode')

    which moves the 'someNode' by 1 unit in the x direction.

    To use the nimble commands module all you need to do is replace the maya commands import with
    the nimble commands import:

        from nimble import cmds

    after which you call commands in the exact same fashion:

        cmds.move(1, 0, 0, 'someNode')
    """

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble import cmds

# Create a sphere
sphereName, sphereShape = cmds.sphere()

# Move the created sphere to x=10
cmds.move(10, 0, 0, sphereName)

