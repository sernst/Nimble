# MayaRouter.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import sys
import inspect

from pyaid.ArgsUtils import ArgsUtils
from pyaid.ModuleUtils import ModuleUtils
from pyaid.dict.DictUtils import DictUtils
from pyaid.reflection.Reflection import Reflection
from pyaid.string.StringUtils import StringUtils

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.router.NimbleRouter import NimbleRouter
from nimble.connection.router.runExec import runMelExec
from nimble.connection.router.runExec import runPythonExec
from nimble.data.NimbleResponseData import NimbleResponseData
from nimble.data.enum.DataErrorEnum import DataErrorEnum
from nimble.data.enum.DataKindEnum import DataKindEnum
from nimble.mayan.NimbleScriptBase import NimbleScriptBase

try:
    # noinspection PyUnresolvedReferences
    import maya.cmds as mc
    # noinspection PyUnresolvedReferences
    import maya.utils as mu
    _runningInMaya = True
except Exception:
    _runningInMaya = False

if sys.version > '3':
    import importlib
    reload = importlib.reload


#___________________________________________________________________________________________________ MayaRouter
class MayaRouter(NimbleRouter):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ createReply
    @classmethod
    def createReply(cls, kind, result, errorMessage =None):
        payload = result if isinstance(result, dict) else {'result':result}
        warnings = ArgsUtils.extract(NimbleEnvironment.REMOTE_RESULT_WARNING_KEY, None, payload)

        if errorMessage:
            return NimbleResponseData(
                kind=kind,
                response=NimbleResponseData.FAILED_RESPONSE,
                warnings=warnings,
                error=errorMessage,
                payload=payload)

        return NimbleResponseData(
            kind=kind,
            warnings=warnings,
            response=NimbleResponseData.SUCCESS_RESPONSE,
            payload=payload )

#___________________________________________________________________________________________________ runPythonImport
    @classmethod
    def runPythonImport(cls, payload):
        try:
            kwargs       = payload.get('kwargs', {})
            targetModule = StringUtils.unicodeToStr(payload['module'])
            targetMethod = StringUtils.unicodeToStr(payload.get('method'))
            targetClass  = StringUtils.unicodeToStr(payload.get('class'))
            target       = targetClass if targetClass is not None else targetMethod
            if target is None:
                parts        = targetModule.rsplit('.', 1)
                targetModule = parts[0]
                target       = parts[1]
        except Exception as err:
            NimbleEnvironment.logError([
                'ERROR: Failed to parse python import payload',
                'PAYLOAD: ' + DictUtils.prettyPrint(payload)], err)
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_IMPORT,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE)

        # Dynamically import the specified module and reload it to make sure any changes have
        # been updated
        try:
            module = ModuleUtils.importModule(targetModule, globals(), locals(), [target])
            reload(module)
            target = getattr(module, target)
        except Exception as err:
            NimbleEnvironment.logError([
                'ERROR: Failed to import python target',
                'MODULE: ' + str(targetModule),
                'TARGET: ' + str(target),
                'PAYLOAD: ' + DictUtils.prettyPrint(payload)], err)
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_IMPORT,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE)

        try:
            result = dict()
            if targetClass is not None:
                tc = target()
                result = getattr(tc, targetMethod)(**kwargs) \
                    if targetMethod else \
                    tc(**kwargs)
            elif targetMethod is not None:
                result = target(**kwargs)
            else:
                # Find a NimbleScriptBase derived class definition and if it exists, run it to
                # populate the results
                for name,value in Reflection.getReflectionDict(target).iteritems():
                    if not inspect.isclass(value):
                        continue

                    if NimbleScriptBase in value.__bases__:
                        result = getattr(target, name)()(**kwargs)
                        found  = True

            # If a result dictionary contains an error key format the response as a failure
            errorMessage = None
            try:
                errorMessage = ArgsUtils.extract(
                    NimbleEnvironment.REMOTE_RESULT_ERROR_KEY, None, result)
            except Exception as err:
                pass

            return cls.createReply(DataKindEnum.PYTHON_IMPORT, result, errorMessage=errorMessage)
        except Exception as err:
            msg = 'ERROR: Failed to execute remote script'
            NimbleEnvironment.logError([
                msg,
                'PAYLOAD: ' + DictUtils.prettyPrint(payload),
                'TARGET: ' + str(target)], err)
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_IMPORT,
                error=msg + ': ' + str(err),
                response=NimbleResponseData.FAILED_RESPONSE)

#___________________________________________________________________________________________________
    @classmethod
    def processRequest(cls, data):
        result = None
        if data.kind == DataKindEnum.MEL_SCRIPT:
            result = mu.executeInMainThreadWithResult(runMelExec, data.payload['script'])
        elif data.kind == DataKindEnum.PYTHON_SCRIPT:
            result = mu.executeInMainThreadWithResult(
                runPythonExec,
                data.payload['script'],
                data.payload['kwargs'])
        elif data.kind == DataKindEnum.MAYA_COMMAND:
            result = mu.executeInMainThreadWithResult(
                cls._executeMayaCommand,
                data.payload)
        elif data.kind == DataKindEnum.MAYA_COMMAND_BATCH:
            result = mu.executeInMainThreadWithResult(
                cls._executeMayaCommandBatch,
                data.payload)
        elif data.kind == DataKindEnum.COMMAND:
            result = mu.executeInMainThreadWithResult(
                cls._executeCommand,
                data.payload)
        elif data.kind == DataKindEnum.PYTHON_SCRIPT_FILE:
            result = mu.executeInMainThreadWithResult(
                cls._runPythonFile,
                data.payload)
        elif data.kind == DataKindEnum.PYTHON_IMPORT:
            result = mu.executeInMainThreadWithResult(
                cls.runPythonImport,
                data.payload)

        if result:
            if isinstance(result, NimbleResponseData):
                return result
            return cls.createReply(data.kind, result)

        return None

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _routeMessage
    def _routeMessageImpl(self, data):
        return self.processRequest(data)

#___________________________________________________________________________________________________ _executeCommand
    @classmethod
    def _executeCommand(cls, payload):
        cmd = payload['command']
        if cmd is None or (StringUtils.isStringType(cmd) and not cmd in globals()):
            return NimbleResponseData(
                    kind=DataKindEnum.COMMAND,
                    response=NimbleResponseData.FAILED_RESPONSE,
                    error=DataErrorEnum.INVALID_COMMAND )

        if StringUtils.isStringType(cmd):
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
                        raise Exception(
                            '%s not found on %s. Unable to execute command.' % \
                            (str(method), str(target) ))
            except Exception as err:
                return NimbleResponseData(
                    kind=DataKindEnum.COMMAND,
                    response=NimbleResponseData.FAILED_RESPONSE,
                    error=str(err) )

            if method:
                targetObject = getattr(Target, method)
                if inspect.ismethod(targetObject) and targetObject.__self__ is None:
                    targetObject = getattr(cls._instantiateClass(Target, cmd), method)
            elif inspect.isclass(Target):
                targetObject = cls._instantiateClass(Target, cmd)
            else:
                targetObject = Target

        try:
            result = targetObject(
                *payload['args'],
                **DictUtils.cleanDictKeys(payload['kwargs']) )
            return cls.createReply(DataKindEnum.COMMAND, result)
        except Exception as err:
            return NimbleResponseData(
                kind=DataKindEnum.COMMAND,
                response=NimbleResponseData.FAILED_RESPONSE,
                error=str(err) )

#___________________________________________________________________________________________________ _instantiateClass
    @classmethod
    def _instantiateClass(cls, Target, command):
        k = 'constructorArgs'
        conArgs = command[k] if k in command else None

        k = 'constructorKwargs'
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
    @classmethod
    def _executeMayaCommand(cls, payload, createReply =True):
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
                return cls.createReply(DataKindEnum.MAYA_COMMAND, result)
            else:
                return result
        except Exception as err:
            return NimbleResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE )

#___________________________________________________________________________________________________ _executeMayaCommandBatch
    @classmethod
    def _executeMayaCommandBatch(cls, payload):
        out = []
        for item in payload['commands']:
            result = cls._executeMayaCommand(item, createReply=False)
            if not isinstance(result, NimbleResponseData):
                out.append(result)
            elif not result.success:
                return result
            else:
                out.append(result.payload['result'])

        return out

#___________________________________________________________________________________________________ _runPythonFile
    @classmethod
    def _runPythonFile(cls, payload):
        try:
            path = payload['path']
            if path.endswith('.py'):
                f = open(path, 'r')
            else:
                f = open(path, 'rb')
            script = f.read()
            f.close()
        except Exception as err:
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_SCRIPT_FILE,
                error=str(err),
                response=NimbleResponseData.FAILED_RESPONSE)

        if not script:
            return NimbleResponseData(
                kind=DataKindEnum.PYTHON_SCRIPT_FILE,
                error='Empty or missing script file at: ' + str(payload['path']),
                response=NimbleResponseData.FAILED_RESPONSE)

        return runPythonExec(script, payload['kwargs'])

