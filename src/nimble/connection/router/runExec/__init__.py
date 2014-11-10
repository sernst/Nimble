# __init__.py
# (C)2012-2014
# Scott Ernst

import inspect
import imp

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.reflection.Reflection import Reflection

import nimble
# AS NEEDED: from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.mayan.NimbleScriptBase import NimbleScriptBase

#___________________________________________________________________________________________________ runMelExec
def runMelExec(script):
    try:
        nimble.cmds.undoInfo(openChunk=True)
    except Exception as err:
        return False

    try:
        import maya.mel as mm
        result = mm.eval(script)
    except Exception as err:
        from nimble.data.NimbleResponseData import NimbleResponseData
        from nimble.data.enum.DataKindEnum import DataKindEnum
        result = NimbleResponseData(
            kind=DataKindEnum.MEL_SCRIPT,
            response=NimbleResponseData.FAILED_RESPONSE,
            error=str(err) )

    try:
        nimble.cmds.undoInfo(closeChunk=True)
    except Exception as err:
        return False

    return result

#___________________________________________________________________________________________________ runPythonExec
def runPythonExec(script, kwargs =None):
    from nimble.NimbleEnvironment import NimbleEnvironment
    from nimble.data.NimbleResponseData import NimbleResponseData
    from nimble.data.enum.DataKindEnum import DataKindEnum

    try:
        nimble.cmds.undoInfo(openChunk=True)
    except Exception as err:
        return False

    try:
        # Create a new, temporary module in which to run the script
        module = imp.new_module('runExecTempModule')

        # Initialize the script with script inputs
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
    except Exception as err:
        logger = Logger('runPythonExec', printOut=True)
        logger.writeError('ERROR: Failed Remote Script Execution', err)
        result = NimbleResponseData(
            kind=DataKindEnum.PYTHON_SCRIPT,
            response=NimbleResponseData.FAILED_RESPONSE,
            error=str(err) )

    # If a result dictionary contains an error key format the response as a failure
    try:
        errorMessage = ArgsUtils.extract(
            NimbleEnvironment.REMOTE_RESULT_ERROR_KEY, None, result)
        if errorMessage:
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_SCRIPT,
                response=NimbleResponseData.FAILED_RESPONSE,
                error=errorMessage,
                payload=result)
    except Exception as err:
        pass

    try:
        nimble.cmds.undoInfo(closeChunk=True)
    except Exception as err:
        return False

    return result
