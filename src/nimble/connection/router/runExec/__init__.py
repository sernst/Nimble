# __init__.py
# (C)2012-2014
# Scott Ernst

import inspect
import imp

from pyaid.debug.Logger import Logger
from pyaid.reflection.Reflection import Reflection

import nimble
from nimble.mayan.NimbleScriptBase import NimbleScriptBase

#___________________________________________________________________________________________________ runMelExec
def runMelExec(script):
    try:
        nimble.cmds.undoInfo(openChunk=True)
    except Exception, err:
        return False

    try:
        import maya.mel as mm
        result = mm.eval(script)
    except Exception, err:
        from nimble.data.NimbleResponseData import NimbleResponseData
        from nimble.data.enum.DataKindEnum import DataKindEnum
        result = NimbleResponseData(
            kind=DataKindEnum.MEL_SCRIPT,
            response=NimbleResponseData.FAILED_RESPONSE,
            error=str(err) )

    try:
        nimble.cmds.undoInfo(closeChunk=True)
    except Exception, err:
        return False

    return result

#___________________________________________________________________________________________________ runPythonExec
def runPythonExec(script, kwargs =None):
    try:
        nimble.cmds.undoInfo(openChunk=True)
    except Exception, err:
        return False

    try:
        # Create a new, temporary module in which to run the script
        module = imp.new_module('runExecTempModule')

        # Initialize the script with script inputs
        from nimble.NimbleEnvironment import NimbleEnvironment
        setattr(module, NimbleEnvironment.REMOTE_KWARGS_KEY, kwargs if kwargs is not None else dict())
        setattr(module, NimbleEnvironment.REMOTE_RESULT_KEY, dict())

        # Executes the script in the new module
        exec script in module.__dict__

        # Find a NimbleScriptBase derived class definition and if it exists, run it to populate the
        # results
        for name,value in Reflection.getReflectionDict(module).iteritems():
            if not inspect.isclass(value):
                continue

            if NimbleScriptBase in value.__bases__:
                getattr(module, name)().run()
                break

        # Retrieve the results object that contains all results set by the execution of the script
        result = getattr(module, NimbleEnvironment.REMOTE_RESULT_KEY)
    except Exception, err:
        logger = Logger('runPythonExec', printOut=True)
        logger.writeError('ERROR: Failed Remote Script Execution', err)

        from nimble.data.NimbleResponseData import NimbleResponseData
        from nimble.data.enum.DataKindEnum import DataKindEnum
        result = NimbleResponseData(
            kind=DataKindEnum.PYTHON_SCRIPT,
            response=NimbleResponseData.FAILED_RESPONSE,
            error=str(err) )

    try:
        nimble.cmds.undoInfo(closeChunk=True)
    except Exception, err:
        return False

    return result
