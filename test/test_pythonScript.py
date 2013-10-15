import os
from pyaid.file.FileUtils import FileUtils

import nimble

script = """\
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
"""

#---------------------------------------------------------------------------------------------------
print 'RUNNING SCRIPT:'
conn = nimble.getConnection()
result = conn.runPythonScript(script, offset=20)

print '\tRESULT:', result, type(result)
print '\tPAYLOAD:', result.payload

#---------------------------------------------------------------------------------------------------
print 'RUNNING FILE:'
result = conn.runPythonScriptFile(
    FileUtils.createPath(
        os.path.abspath(os.path.dirname(__file__)), 'pythonTestScript.py', isFile=True),
    offset=5)

print '\tRESULT:', result, type(result)
print '\tPAYLOAD:', result.payload

print 'Operation Complete'
