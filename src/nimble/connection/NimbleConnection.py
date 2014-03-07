# NimbleConnection.py
# (C)2012-2014
# Scott Ernst

import socket
from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils

from pyaid.string.ByteChunk import ByteChunk

import nimble
from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.router.MayaRouter import MayaRouter
from nimble.connection.support.MayaCommandLink import MayaCommandLink
from nimble.connection.support.ImportedCommand import ImportedCommand
from nimble.data.NimbleData import NimbleData
from nimble.data.enum.DataKindEnum import DataKindEnum
from nimble.enum.ConnectionFlags import ConnectionFlags
from nimble.error.MayaCommandException import MayaCommandException
from nimble.utils.SocketUtils import SocketUtils

#___________________________________________________________________________________________________ NimbleConnection
class NimbleConnection(object):
    """Establishes a socket connection with a NimbleServer instance for communication."""

#===================================================================================================
#                                                                                       C L A S S

    _CONNECTION_POOL = []

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """ Creates a new instance of NimbleConnection and opens the communication socket to the
            corresponding NimbleServer instance. NimbleEnvironment is used to determine whether the
            connection should be to a Maya or external application NimbleServer instance. """

        self._active          = False
        self._socket          = None
        self._mayaCommandLink = None
        self._activatedTime   = None
        self._chunk           = ByteChunk(endianess=ByteChunk.BIG_ENDIAN)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: active
    @property
    def active(self):
        """ Specifies whether or not the NimbleConnection instance is active. When active the
            instance can communicate with its remote NimbleServer counterpart. NimbleConnection
            instances are active by default and only become inactive if they are closed after
            which point they will have to be reopened in order to allow further communication. """

        return self._active

#___________________________________________________________________________________________________ GS: mayaCommands
    @property
    def mayaCommands(self):
        """ Access to the local or remove maya command """
        if not self._mayaCommandLink:
            self._mayaCommandLink = MayaCommandLink(connection=self)
        return self._mayaCommandLink

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ echo
    def echo(self, message):
        return self._send(NimbleData(kind=DataKindEnum.ECHO, payload={'echo':message}))

#___________________________________________________________________________________________________ ping
    def ping(self, message =None):
        """Doc..."""
        return self._send(NimbleData(kind=DataKindEnum.PING, payload={'msg':message}))

#___________________________________________________________________________________________________ addToMayaPythonPath
    def addToMayaPythonPath(self, path):
        return self._send(NimbleData(
            kind=DataKindEnum.ADD_SYSTEM_PATH,
            payload={'path':path} ))

#___________________________________________________________________________________________________ runMelScript
    def runMelScript(self, script):
        return self._send(NimbleData(
            kind=DataKindEnum.MEL_SCRIPT,
            payload={'script':script} ))

#___________________________________________________________________________________________________ runPythonScript
    def runPythonScript(self, script, **kwargs):
        return self._send(NimbleData(
            kind=DataKindEnum.PYTHON_SCRIPT,
            payload={'script':script, 'kwargs':kwargs} ))

#___________________________________________________________________________________________________ runPythonScriptFile
    def runPythonScriptFile(self, path, **kwargs):
        return self._send(NimbleData(
            kind=DataKindEnum.PYTHON_SCRIPT_FILE,
            payload={'path':path, 'kwargs':kwargs} ))

#___________________________________________________________________________________________________ runPythonImport
    def runPythonImport(self, modulePackage, methodName =None, className=None, runInMaya =None, **kwargs):
        """ Executes the specified import through Nimble in the specified run mode.

            modulePackage:  (String) An absolute (dot-syntax) formatted import to the module you
                            wish to be executed. This module will be imported by Maya and must be
                            on its sys.path.

            [methodName]:   (String) An optional function name to be executed within the module. If
                            a class name is specified this method will be called on an instance of
                            the specified class. If no class name is specified the method will be
                            called directly on the module.

            [className]:    (String) An optional class name of a class to import within the
                            specified module. The class will be imported from the module and
                            instantiated.

            [runInMaya]:    If True the import will be executed within Maya. If False the import
                            will be executed outside of Maya on the remote end of the Nimble
                            connection. The default value of None will use the current global
                            setting, which can be set by the nimble.enablePythonTestMode()
                            top-level function and defaults to runInMaya = True, i.e. test mode
                            is disabled.

                Returns a NimbleResponseData object with the results of the script execution. """
        payload = {
            'module':modulePackage,
            'method':methodName,
            'class':className,
            'kwargs':kwargs}

        if (NimbleEnvironment.TEST_REMOTE_MODE if runInMaya is None else runInMaya):
            return MayaRouter.runPythonImport(payload)
        else:
            return self._send(NimbleData(kind=DataKindEnum.PYTHON_IMPORT, payload=payload))

#___________________________________________________________________________________________________ runPythonClass
    def runPythonClass(self, targetClass, methodName =None, runInMaya =None, **kwargs):
        """ Convenience method that wraps runPythonImport where the targetClass is a Class object
            that is parsed into a modulePackage and className.

            targetClass:    (Class) A class object that should be executed in Nimble.

            For additional information see NimbleConnection.runPythonImport """
        return self.runPythonImport(
            modulePackage=targetClass.__module__,
            methodName=methodName,
            className=targetClass.__name__,
            runInMaya=runInMaya, **kwargs)

#___________________________________________________________________________________________________ runPythonModule
    def runPythonModule(self, module, methodName =None, className =None, runInMaya =None, **kwargs):
        """ Convenience method that wraps runPythonImport where the module is an imported module
            object instead of the string to the modulePackage.

            module:    (Module) A module object that is parsed into a package name.

            For additional information see NimbleConnection.runPythonImport """
        return self.runPythonImport(
            modulePackage=module.__name__,
            methodName=methodName,
            className=className,
            runInMaya=runInMaya, **kwargs)

#___________________________________________________________________________________________________ maya
    def maya(self, command, *args, **kwargs):
        result = self.runMayaCommand(command, *args, **kwargs)
        if not result or not result.success:
            raise MayaCommandException(
                'Failed execution of Maya command: ' + str(command),
                response=result)
        return result.payload['result']

#___________________________________________________________________________________________________ runMayaCommand
    def runMayaCommand(self, command, *args, **kwargs):
        return self._send(NimbleData(
            kind=DataKindEnum.MAYA_COMMAND,
            payload={
                'command':str(command),
                'kwargs':kwargs,
                'args':args} ))

#___________________________________________________________________________________________________ runMayaCommandBatch
    def runMayaCommandBatch(self, commandList):
        return self._send(NimbleData(
            kind=DataKindEnum.MAYA_COMMAND_BATCH,
            payload={'commands':commandList} ))

#___________________________________________________________________________________________________ mayaBatch
    def mayaBatch(self, commandList):
        result = self.runMayaCommandBatch(commandList)
        if not result or not result.success:
            raise MayaCommandException(
                'Failed execution during Maya command batch execution',
                response=result)
        return result.payload['result']

#___________________________________________________________________________________________________ command
    def command(self, command, *args, **kwargs):
        result = self.runCommand(command, *args, **kwargs)
        if not result or not result.success:
            raise MayaCommandException(
                'Failed execution of command: ' + str(command),
                response=result)
        return result.payload['result']

#___________________________________________________________________________________________________ runCommand
    def runCommand(self, command, *args, **kwargs):
        return self._send(NimbleData(
            kind=DataKindEnum.COMMAND,
            payload={
                'command':command.toDict() if isinstance(command, ImportedCommand) else str(command),
                'kwargs':kwargs,
                'args':args } ))

#___________________________________________________________________________________________________ close
    def close(self):
        if not self._active:
            return False

        self._active = False
        self._socket.close()

        if self in NimbleConnection._CONNECTION_POOL:
            NimbleConnection._CONNECTION_POOL.remove(self)

        return True

#___________________________________________________________________________________________________ open
    def open(self):
        if self._active:
            nowTime = TimeUtils.getNowSeconds()
            if nowTime - self._activatedTime > NimbleEnvironment.CONNECTION_LIFETIME:
                self.close()
            else:
                return False

        self._activatedTime = TimeUtils.getNowSeconds()
        try:
            target = ('localhost', NimbleEnvironment.getConnectionPort())
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Sets socket option to prevent connection being refused by TCP reconnecting
            # to the same socket after a recent closure.
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setblocking(1)
            self._socket.connect(target)
        except Exception, err:
            NimbleEnvironment.logError(
                '[ERROR | NIMBLE COMMUNICATION] Failed to open Nimble connection', err)
            return False

        if self not in NimbleConnection._CONNECTION_POOL:
            NimbleConnection._CONNECTION_POOL.append(self)

        self._active = True
        return True

#___________________________________________________________________________________________________ getConnection
    @classmethod
    def getConnection(cls, forceCreate =False, **kwargs):
        if forceCreate or not NimbleConnection._CONNECTION_POOL:
            return NimbleConnection(**kwargs)

        return NimbleConnection._CONNECTION_POOL[-1]

#___________________________________________________________________________________________________ closeConnectionPool
    @classmethod
    def closeConnectionPool(cls):
        while NimbleConnection._CONNECTION_POOL:
            NimbleConnection._CONNECTION_POOL.pop().close()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _send
    def _send(self, nimbleData):
        """Doc..."""
        responseFlags = 0
        message       = u''
        retry         = NimbleEnvironment.REMOTE_RETRY_COUNT

        while retry > 0:
            try:
                self.open()
            except Exception, err:
                failure = [
                    '[ERROR | NIMBLE COMMUNICATION] Unable to open connection',
                    err ]
                retry -= 1
                if retry == 0:
                    if not nimble.quietFailure:
                        NimbleEnvironment.logError(failure[0], failure[1])
                    return None
                continue

            try:
                serialData = nimbleData.serialize()
            except Exception, err:
                failure = [
                    '[ERROR | NIMBLE COMMUNICATION] Unable to serialize data for transmission',
                    err ]
                if not nimble.quietFailure:
                    NimbleEnvironment.logError(failure[0], failure[1])
                return None

            try:
                self._chunk.clear()
                self._chunk.writeUint32(NimbleEnvironment.CONNECTION_FLAGS)
                self._chunk.writeString(serialData + NimbleEnvironment.TERMINATION_IDENTIFIER)
                self._socket.sendall(self._chunk.chunk)
            except Exception, err:
                failure = [
                    '[ERROR | NIMBLE COMMUNICATION] Unable to send data',
                    err ]
                self.close()
                retry -= 1
                if retry == 0:
                    if not nimble.quietFailure:
                        NimbleEnvironment.logError(failure[0], failure[1])
                    return None
                continue

            try:
                self._chunk.clear()
                self._chunk.writeString(SocketUtils.receiveInChunks(
                    self._socket,
                    chunkSize=NimbleEnvironment.SOCKET_RESPONSE_CHUNK_SIZE) )
                self._chunk.position = 0
                responseFlags  = self._chunk.readUint32()
                message        = StringUtils.strToUnicode(str(self._chunk.read(-1)))

                # Break while loop on successful reading of the result
                if message is not None:
                    break

            except Exception, err:
                if not nimble.quietFailure:
                    NimbleEnvironment.logError(
                        '[ERROR | NIMBLE COMMUNICATION] Unable to read response', err)
                self.close()
                return None

        try:
            if not (responseFlags & ConnectionFlags.KEEP_ALIVE):
                self.close()
        except Exception, err:
            if not nimble.quietFailure:
                NimbleEnvironment.logError(
                    '[ERROR | NIMBLE COMMUNICATION] Unable to close connection', err)

        try:
            return NimbleData.fromMessage(message)
        except Exception, err:
            if not nimble.quietFailure:
                NimbleEnvironment.logError(
                    '[ERROR | NIMBLE COMMUNICATION] Response data parsing failure', err)
            return None

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __del__
    def __del__(self):
        try:
            self._socket.close()
        except Exception, err:
            pass

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
