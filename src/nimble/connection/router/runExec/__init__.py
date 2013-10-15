# __init__.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

import imp

import nimble

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
        module = imp.new_module('runExecTempModule')

        from nimble.NimbleEnvironment import NimbleEnvironment
        setattr(module, NimbleEnvironment.REMOTE_KWARGS_KEY, kwargs if kwargs is not None else dict())
        setattr(module, NimbleEnvironment.REMOTE_RESULT_KEY, dict())

        exec script in module.__dict__
        result = getattr(module, NimbleEnvironment.REMOTE_RESULT_KEY)
    except Exception, err:
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
