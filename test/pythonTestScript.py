import nimble

from nimble import cmds
result = cmds.polySphere()
name = result[0]

cmds.move(-10, -10, -10, name)
cmds.rotate(50, 20, 10, name)
cmds.scale(2, 2, 2, name)

response = nimble.createRemoteResponse(globals())
response.put('name', name)
