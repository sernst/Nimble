# MayaRouter.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

import inspect

import maya.cmds as mc
import maya.utils as mu

from nimble.connection.router.NimbleRouter import NimbleRouter
from nimble.connection.router.runExec import runMelExec
from nimble.connection.router.runExec import runPythonExec
from nimble.data.NimbleResponseData import NimbleResponseData
from nimble.data.enum.DataErrorEnum import DataErrorEnum
from nimble.data.enum.DataKindEnum import DataKindEnum
from nimble.utils.DictUtils import DictUtils

#___________________________________________________________________________________________________ MayaRouter
class MayaRouter(NimbleRouter):
    """A class for..."""

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _routeMessage
    def _routeMessage(self, data):

        result = None
        if data.kind == DataKindEnum.MEL_SCRIPT:
            result = mu.executeInMainThreadWithResult(runMelExec, data.payload['script'])
        elif data.kind == DataKindEnum.PYTHON_SCRIPT:
            result = mu.executeInMainThreadWithResult(runPythonExec, data.payload['script'])
        elif data.kind == DataKindEnum.MAYA_COMMAND:
            result = mu.executeInMainThreadWithResult(self._executeMayaCommand, data.payload)
        elif data.kind == DataKindEnum.MAYA_COMMAND_BATCH:
            result = mu.executeInMainThreadWithResult(self._executeMayaCommandBatch, data.payload)
        elif data.kind == DataKindEnum.COMMAND:
            result = mu.executeInMainThreadWithResult(self._executeCommand, data.payload)
        elif data.kind == DataKindEnum.PYTHON_SCRIPT_FILE:
            result = mu.executeInMainThreadWithResult(self._runPythonFile, data.payload)

        if result:
            if isinstance(result, NimbleResponseData):
                return result
            return self._createReply(data.kind, result)

        return None

#___________________________________________________________________________________________________ _createReply
    def _createReply(self, kind, result):
        return NimbleResponseData(
            kind=kind,
            response=NimbleResponseData.SUCCESS_RESPONSE,
            payload={'result':result} )

#___________________________________________________________________________________________________ _executeCommand
    def _executeCommand(self, payload):
        cmd = payload['command']
        if cmd is None or (isinstance(cmd, basestring) and not cmd in globals()):
            return NimbleResponseData(
                    kind=DataKindEnum.COMMAND,
                    response=NimbleResponseData.FAILED_RESPONSE,
                    error=DataErrorEnum.INVALID_COMMAND )

        if isinstance(cmd, basestring):
            targetObject = globals().get(cmd)
        else:
            if isinstance(cmd, dict):
                module = str(cmd['module'])
                target = str(cmd['target'])
                method = str(cmd['method']) if 'method' in cmd else None
            else:
                target = str(cmd[0])
                module = str(cmd[1]) if len(cmd) > 0 else None
                method = str(cmd[2]) if len(cmd) > 1 else None

            try:
                res    = __import__(module, globals(), locals(), [target])
                Target = getattr(res, target)
                if method:
                    m = getattr(Target, method)
                    if m is None:
                        raise Exception, '%s not found on %s. Unable to execute command.' % \
                                         (str(method), str(target))
            except Exception, err:
                return NimbleResponseData(
                    kind=DataKindEnum.COMMAND,
                    response=NimbleResponseData.FAILED_RESPONSE,
                    error=str(err) )

            if method:
                targetObject = getattr(Target, method)
                if inspect.ismethod(targetObject) and targetObject.__self__ is None:
                    targetObject = getattr(self._instantiateClass(Target, cmd), method)
            elif inspect.isclass(Target):
                targetObject = self._instantiateClass(Target, cmd)
            else:
                targetObject = Target

        try:
            result = targetObject(
                *payload['args'],
                **DictUtils.cleanDictKeys(payload['kwargs']) )
            return self._createReply(DataKindEnum.COMMAND, result)
        except Exception, err:
            return NimbleResponseData(
                kind=DataKindEnum.COMMAND,
                response=NimbleResponseData.FAILED_RESPONSE,
                error=str(err) )

#___________________________________________________________________________________________________ _instantiateClass
    def _instantiateClass(self, Target, command):
        k       = 'constructorArgs'
        conArgs = command[k] if k in command else None

        k         = 'constructorKwargs'
        conKwargs = command[k] if k in command else None

        if conArgs and conKwargs:
            targetObject = Target(*conArgs, **DictUtils.cleanDictKeys(conKwargs))
        elif conArgs:
            targetObject = Target(*conArgs)
        elif conKwargs:
            targetObject = Target(**DictUtils.cleanDictKeys(conKwargs))
        else:
            targetObject = Target()

        return targetObject

#___________________________________________________________________________________________________ _executeMayaCommand
    def _executeMayaCommand(self, payload, createReply =True):
        cmd = getattr(mc, str(payload['command']), None)
        if cmd is None:
            return NimbleResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                error=DataErrorEnum.UNRECOGNIZED_MAYA_COMMAND,
                response=NimbleResponseData.FAILED_RESPONSE )

        try:
            result = cmd(
                *payload['args'],
                **DictUtils.cleanDictKeys(payload['kwargs']) )
            if createReply:
                return self._createReply(DataKindEnum.MAYA_COMMAND, result)
            else:
                return result
        except Exception, err:
            return NimbleResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE )

#___________________________________________________________________________________________________ _executeMayaCommandBatch
    def _executeMayaCommandBatch(self, payload):
        out = []
        for item in payload['commands']:
            result = self._executeMayaCommand(item, createReply=False)
            if not isinstance(result, NimbleResponseData):
                out.append(result)
            elif not result.success:
                return result
            else:
                out.append(result.payload['result'])

        return out

#___________________________________________________________________________________________________ _runPythonFile
    def _runPythonFile(self, payload):
        try:
            f      = open(payload['path'], 'r')
            script = f.read()
            f.close()
        except Exception, err:
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_SCRIPT_FILE,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE)

        return runPythonExec(script)
