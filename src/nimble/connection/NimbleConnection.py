# NimbleConnection.py
# (C)2012-2014
# Scott Ernst

import socket

import nimble
from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.support.MayaCommandLink import MayaCommandLink
from nimble.connection.support.ImportedCommand import ImportedCommand
from nimble.data.NimbleData import NimbleData
from nimble.data.enum.DataKindEnum import DataKindEnum
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

        self._active = False
        self._socket = None

        if not NimbleEnvironment.inMaya():
            self.open()

        self._mayaCommandLink = None

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
                response=result
            )
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
            return False

        try:
            target = ('localhost', NimbleEnvironment.getConnectionPort())
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Sets socket option to prevent connection being refused by TCP reconnecting
            # to the same socket after a recent closure.
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.connect(target)
        except Exception, err:
            print 'Failed to open Nimble connection.'
            print err
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
        message = u''
        retry   = 3
        failure = None

        while retry > 0:
            try:
                self.open()
            except Exception, err:
                failure = [
                    '[ERROR] Nimble communication failure: Unable to open connection',
                    err ]
                retry -= 1
                if retry == 0:
                    if not nimble.quietFailure:
                        print failure[0] + '\n  ', failure[1]
                    return None
                continue

            try:
                serialData = nimbleData.serialize()
            except Exception, err:
                failure = [
                    '[ERROR] Nimble communication failure: Unable to serialize data for transmission',
                    err ]
                if not nimble.quietFailure:
                    print failure[0] + '\n  ', failure[1]
                return None

            try:
                SocketUtils.sendInChunks(self._socket, serialData)
            except Exception, err:
                failure = [
                    '[ERROR] Nimble communication failure: Unable to send data',
                    err ]
                self.close()
                retry -= 1
                if retry == 0:
                    if not nimble.quietFailure:
                        print failure[0] + '\n  ', failure[1]
                    return None
                continue

            try:
                message = SocketUtils.receiveInChunks(
                    self._socket,
                    chunkSize=NimbleEnvironment.SOCKET_RESPONSE_CHUNK_SIZE)

                # Break while loop on successful reading of the result
                if message is not None:
                    break

            except Exception, err:
                if not nimble.quietFailure:
                    print '[ERROR] Nimble communication failure: Unable to read response'
                    print '  ', err
                self.close()
                return None

        try:
            self.close()
        except Exception, err:
            if not nimble.quietFailure:
                print '[ERROR] Nimble communication failure: Unable to close connection'
                print '  ', err

        try:
            return NimbleData.fromMessage(message)
        except Exception, err:
            if not nimble.quietFailure:
                print 'Nimble communication data failure.'
                print '  ', err
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
