Nimble
======

A remote communication bridge between independent Python interpreters and Maya's Python Interpreter.

Nimble enables transparent execution of Maya commands, both built-in and custom-made, from an external Python interpreter no matter the version or platform differences bewtween this external interpreter and Maya's built-in interpreter. At the same time Nimble can be run within the Maya Python interpreter directly, so code developed with Nimble works in both external and Maya Python interpreters in a completely transparent fashion.

Nimble allows you to:

 * Procedurally control Maya from a more easily customized version of Python, with access to many more packages and capabilities. 
 * Debug Maya Python scripts from any Python debugger with absolutely no setup.
 * Develop remotely in any debugger and then run natively inside of Python with absolutely no re-coding.
 * Test and iterate code without relaunching Maya or manually handling package reloads with every change.
 * Build richer scripts that you can share and distribute without the overhead of custom modification of Maya's Python packages.
 * Build richer GUIs written in any GUi toolkit supported by Python.

Overview
--------

Nimble requires another package (PyAid)[https://github.com/sernst/PyAid] to be installed as well. Like Nimble, these are not distributed as pip packages because older versions of the Maya Python Interpreter did not readily support custom package installation. Instead the installation/configuration step required is to clone or download these packages and add the two libraries to the PYTHONPATH variable in your Maya.env environment file (as well as any remote Python interpreter that may use them):

```
# Windows
PYTHONPATH=c:\\path\to\Nimble\src;c:\\path\to\PyAid\src;

# OSX/Linux 
PYTHONPATH=/path/to/Nimble/src;/path/to/PyAid/src;
```

Then, after opening Maya, run the commands:

```python
import nimble
nimble.startServer()
```

This starts the nimble service inside your Python environment. Once loaded, the event-based server will wait for external communication.

A nimble script looks like this:

```python
from nimble import cmds

result = cmds.polyCube(height=10, depth=25)
cmds.move(10, 10, 5, result[0])
print 'Translate:', cmds.getAttr(result[0] + '.translate')[0]
```

As you can see the only difference between a nimble script and a standard Maya version is the import statement.

It really is that simple! 

## Custom Ports

By default Nimble uses port `7800` and `7801` for communication between Maya and the remote Nimble environment. If these ports are unavailable in your environment, or you wish to run multiple instances at the same time, ports can be customized.

Make sure that you set the custom ports in both Maya:

```python
# Start a server with custom ports:

import nimble

nimble.startServer(mayaPort=8700, externalPort=8701)
```

and in your remote Nimble environment:

```python
# Set custom ports in a remote Nimble script before calling any other nimble commands

import nimble
from nimble import cmds

nimble.setPorts(maya=8700, external=8701)

result = cmds.polyCube(height=10, depth=25)
```





