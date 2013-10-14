import os
from pyaid.file.FileUtils import FileUtils

import nimble

script = """\
import nimble

from nimble import cmds
result = cmds.polySphere()
name = result[0]

cmds.move(10, 10, 10, name)
cmds.rotate(50, 20, 10, name)
cmds.scale(2, 2, 2, name)

response = nimble.createRemoteResponse(globals())
response.put('name', name)
"""

#---------------------------------------------------------------------------------------------------
print 'RUNNING SCRIPT:'
conn = nimble.getConnection()
result = conn.runPythonScript(script)

print '\tRESULT:', result, type(result)
print '\tPAYLOAD:', result.payload

#---------------------------------------------------------------------------------------------------
print 'RUNNING FILE:'
result = conn.runPythonScriptFile(FileUtils.createPath(
    os.path.abspath(os.path.dirname(__file__)), 'pythonTestScript.py', isFile=True) )

print '\tRESULT:', result, type(result)
print '\tPAYLOAD:', result.payload

print 'Operation Complete'
