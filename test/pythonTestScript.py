import nimble
from nimble import cmds

kwargs = nimble.getRemoteKwargs(globals())

result = cmds.polySphere()
name = result[0]

offset = kwargs.get('offset', 10)

cmds.move(offset, offset, offset, name)
cmds.rotate(50, 20, 10, name)
cmds.scale(2, 2, 2, name)

response = nimble.createRemoteResponse(globals())
response.put('name', name)
response.put('offset', offset)
