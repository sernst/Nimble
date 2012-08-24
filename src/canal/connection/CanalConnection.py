# CanalConnection.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

import socket

from canal.CanalEnvironment import CanalEnvironment
from canal.connection.support.MayaCommandLink import MayaCommandLink
from canal.data.CanalData import CanalData
from canal.data.enum.DataKindEnum import DataKindEnum
from canal.error.MayaCommandException import MayaCommandException

#___________________________________________________________________________________________________ CanalConnection
class CanalConnection(object):
    """Establishes a socket connection with a CanalServer instance for communication."""

#===================================================================================================
#                                                                                       C L A S S

    _CONNECTION_POOL = []

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """ Creates a new instance of CanalConnection and opens the communication socket to the
            corresponding CanalServer instance. CanalEnvironment is used to determine whether the
            connection should be to a Maya or external application CanalServer instance.
        """

        self._active = False
        self._socket = None
        self.open()

        self._mayaCommandLink = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: active
    @property
    def active(self):
        """ Specifies whether or not the CanalConnection instance is active. When active the
            instance can communicate with its remote CanalServer counterpart. CanalConnection
            instances are active by default and only become inactive if they are closed after
            which point they will have to be reopened in order to allow further communication.
        """

        return self._active

#___________________________________________________________________________________________________ GS: mayaCommands
    @property
    def mayaCommands(self):
        """ Access to the local or remove maya command
        """
        if not self._mayaCommandLink:
            self._mayaCommandLink = MayaCommandLink(connection=self)
        return self._mayaCommandLink

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ ping
    def ping(self, message =None):
        """Doc..."""
        return self._send(CanalData(kind=DataKindEnum.PING, payload={'msg':message}))

#___________________________________________________________________________________________________ maya
    def maya(self, command, *args, **kwargs):
        result = self.sendMayaCommand(command, *args, **kwargs)
        if not result or not result.success:
            raise MayaCommandException(
                'Failed execution of Maya command: ' + str(command),
                response=result
            )
        return result.payload['result']

#___________________________________________________________________________________________________ sendMayaCommand
    def sendMayaCommand(self, command, *args, **kwargs):
        return self._send(CanalData(
            kind=DataKindEnum.MAYA_COMMAND,
            payload={
                'command':str(command),
                'kwargs':kwargs,
                'args':args
            }
        ))

#___________________________________________________________________________________________________ close
    def close(self):
        if not self._active:
            return False

        self._active = False
        self._socket.close()

        if self in CanalConnection._CONNECTION_POOL:
            CanalConnection._CONNECTION_POOL.remove(self)

        return True

#___________________________________________________________________________________________________ open
    def open(self):
        if self._active:
            return False

        try:
            target = ('localhost', CanalEnvironment.getConnectionPort())
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(target)
        except Exception, err:
            print 'Failed to open Canal connection.'
            print err
            return False

        if self not in CanalConnection._CONNECTION_POOL:
            CanalConnection._CONNECTION_POOL.append(self)

        self._active = True
        return True

#___________________________________________________________________________________________________ getConnection
    @classmethod
    def getConnection(cls, forceCreate =False, **kwargs):
        if forceCreate or not CanalConnection._CONNECTION_POOL:
            return CanalConnection(**kwargs)

        return CanalConnection._CONNECTION_POOL[-1]

#___________________________________________________________________________________________________ closeConnectionPool
    @classmethod
    def closeConnectionPool(cls):
        while CanalConnection._CONNECTION_POOL:
            CanalConnection._CONNECTION_POOL.pop().close()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _send
    def _send(self, canalData):
        """Doc..."""
        try:
            self._socket.sendall(canalData.serialize())
            message = self._socket.recv(4096)
        except Exception, err:
            print 'Canal communication failure.'
            print err
            return None

        try:
            return CanalData.fromMessage(message)
        except Exception, err:
            print 'Canal communication data failure.'
            print err
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
