# __init__.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import nimble
import imp

#___________________________________________________________________________________________________ runMelExec
def runMelExec(script):
    try:
        nimble.cmds.undoInfo(openChunk=True)
    except Exception, err:
        return False

    success = True

    try:
        import maya.mel as mm
        mm.eval(script)
    except Exception, err:
        from nimble.data.NimbleResponseData import NimbleResponseData
        from nimble.data.enum.DataKindEnum import DataKindEnum
        success = NimbleResponseData(
            kind=DataKindEnum.MEL_SCRIPT,
            response=NimbleResponseData.FAILED_RESPONSE,
            error=str(err)
        )

    try:
        nimble.cmds.undoInfo(closeChunk=True)
    except Exception, err:
        return False

    return success

#___________________________________________________________________________________________________ runPythonExec
def runPythonExec(script):
    try:
        nimble.cmds.undoInfo(openChunk=True)
    except Exception, err:
        return False

    success = True
    try:
        module = imp.new_module('runExecTempModule')
        exec script in module.__dict__
    except Exception, err:
        from nimble.data.NimbleResponseData import NimbleResponseData
        from nimble.data.enum.DataKindEnum import DataKindEnum
        success = NimbleResponseData(
            kind=DataKindEnum.PYTHON_SCRIPT,
            response=NimbleResponseData.FAILED_RESPONSE,
            error=str(err)
        )

    try:
        nimble.cmds.undoInfo(closeChunk=True)
    except Exception, err:
        return False

    return success
