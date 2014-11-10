# helloPythonImport.py
# (C)2014
# Scott Ernst

""" This example shows how to use the advanced import scripting in Nimble. """

from __future__ import print_function, absolute_import, unicode_literals, division

import sys

from pyaid.file.FileUtils import FileUtils

import nimble

# Add the src path for this example to the python system path for access to the scripts
scriptPath = FileUtils.createPath(FileUtils.getDirectoryOf(__file__), 'src', isDir=True)
sys.path.append(scriptPath)

from helloPythonImportExample.scripts import CreateSpheres

# Create a Nimble connection object. This object will be used to send and receive across the
# nimble communication bridge between this script and the Nimble server running in Maya
conn = nimble.getConnection()

# Add the script src path to the Maya Python environment as well so that it can import and run
# the scripts directly
result = conn.addToMayaPythonPath(scriptPath)
if not result.success:
    print('Unable to modify Maya Python path. Are you sure Maya is running a Nimble server?')
    print(result)
    sys.exit(1)

# Now run the CreateSpheres Nimble script creating a ring of 3 spheres. The CreateSpheres module,
# not the class is passed into the runPythonModule.
#
# You don't need to pass in the class or method name because Nimble automatically recognizes that
# the module contains a class that extends NimbleScriptBase exists in the module and knows how
# to properly execute that class.
result = conn.runPythonModule(CreateSpheres, count=4)
if not result.success:
    print('Oh no, something went wrong!', result)
    sys.exit(1)

# This command does the same thing as the previous call (except for the count and y changes) but
# now the class is passed directly instead of the module. You can use either form depending on
# how you prefer to import the source.
result = conn.runPythonClass(CreateSpheres.CreateSpheres, count=6, y=2)

if not result.success:
    print('Oh no, something went wrong!', result)
    sys.exit(1)
else:
    print(result.payload['ringName'] + ':', result.payload['sphereNames'])

# Another example of how to call this command, by specifying the module import path directly. The
# benefit of this form is that you don't need to import the module or class within this script, but
# the trade-off is that your defining the location of the module in a string, which can be harder
# to manage when refactoring.
result = conn.runPythonImport('helloPythonImportExample.scripts.CreateSpheres', count=8, y=4)

if not result.success:
    print('Oh no, something went wrong!', result)
    sys.exit(1)
else:
    print(result.payload['ringName'] + ':', result.payload['sphereNames'])

# We can run these same commands outside of Maya, which is useful when you are developing and debugging
# a script because nothing is imported on the Maya end meaning you don't have to restart or reload
# the script each time you make a change. The downside is that the script will run much slower
# because each command has to sent to Maya instead of running the entire thing inside Maya's Python
# interpreter.
#
# To run outside of maya set the runInMaya named argument to False
result = conn.runPythonModule(CreateSpheres, runInMaya=False, count=10, y=6)

if not result.success:
    print('Oh, no, something went wrong!', result)
    sys.exit(1)
else:
    print(result.payload['ringName'] + ':', result.payload['sphereNames'])

# You can also make all of these commands run outside of Maya by default by enabling PythonTestMode,
# which defaults the runInMaya argument for each command to False.
#
# When enabled all subsequent conn.runPython* calls will run outside of Maya
nimble.enablePythonTestMode(True)

result = conn.runPythonModule(CreateSpheres, count=12, y=8)

if not result.success:
    print('Oh, no, something went wrong!', result)
    sys.exit(1)
else:
    print(result.payload['ringName'] + ':', result.payload['sphereNames'])

# Of course, you can override this default behavior for any command by specifying the runInMaya
# argument explicitly.
result = conn.runPythonModule(CreateSpheres, runInMaya=True, count=15, y=10)

if not result.success:
    print('Oh, no, something went wrong!', result)
    sys.exit(1)
else:
    print(result.payload['ringName'] + ':', result.payload['sphereNames'])

print('Example Complete')
