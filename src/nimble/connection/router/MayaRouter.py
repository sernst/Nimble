# MayaRouter.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import inspect

import maya.cmds as mc
import maya.utils as mu

from nimble.connection.router.NimbleRouter import NimbleRouter
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
        if data.kind == DataKindEnum.MAYA_COMMAND:
            result = mu.executeInMainThreadWithResult(self._executeMayaCommand, data.payload)
        elif data.kind == DataKindEnum.COMMAND:
            result = mu.executeInMainThreadWithResult(self._executeCommand, data.payload)

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
            payload={'result':result}
        )

#___________________________________________________________________________________________________ _executeCommand
    def _executeCommand(self, payload):
        cmd = payload['command']
        if cmd is None or (isinstance(cmd, basestring) and not cmd in globals()):
            return NimbleResponseData(
                    kind=DataKindEnum.COMMAND,
                    response=NimbleResponseData.FAILED_RESPONSE,
                    error=DataErrorEnum.INVALID_COMMAND
            )

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
                    error=str(err)
                )

            if method:
                targetObject = getattr(Target, method)
                if inspect.ismethod(targetObject) and targetObject.__self__ is None:
                    targetObject = getattr(Target(), method)
            elif inspect.isclass(Target):
                targetObject = Target()
            else:
                targetObject = Target

        try:
            result = targetObject(
                *payload['args'],
                **DictUtils.cleanDictKeys(payload['kwargs'])
            )
            return self._createReply(DataKindEnum.COMMAND, result)
        except Exception, err:
            return NimbleResponseData(
                kind=DataKindEnum.COMMAND,
                response=NimbleResponseData.FAILED_RESPONSE,
                error=str(err)
            )

#___________________________________________________________________________________________________ _executeMayaCommand
    def _executeMayaCommand(self, payload):
        cmd = getattr(mc, str(payload['command']), None)
        if cmd is None:
            return NimbleResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                error=DataErrorEnum.UNRECOGNIZED_MAYA_COMMAND,
                response=NimbleResponseData.FAILED_RESPONSE
            )

        try:
            result = cmd(
                *payload['args'],
                **DictUtils.cleanDictKeys(payload['kwargs'])
            )
            return self._createReply(DataKindEnum.MAYA_COMMAND, result)
        except Exception, err:
            return NimbleResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE
            )

