# CanalHandler.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

import asyncore

from canal.CanalEnvironment import CanalEnvironment
from canal.data.CanalData import CanalData
from canal.data.CanalResponseData import CanalResponseData
from canal.data.enum.DataErrorEnum import DataErrorEnum
from canal.data.enum.DataKindEnum import DataKindEnum

#___________________________________________________________________________________________________ CanalRouter
class CanalRouter(asyncore.dispatcher_with_send):

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ handle_read
    def handle_read(self):
        try:
            message  = self.recv(8192)
        except Exception, err:
            return

        if not message:
            return

        logLevel = CanalEnvironment.getServerLogLevel()

        try:
            data = self._parseData(message, logLevel)
        except Exception, err:
            self._sendResponse(
                CanalResponseData(
                    kind=DataKindEnum.GENERAL,
                    error=DataErrorEnum.PARSE_FAILURE,
                    response=CanalResponseData.FAILED_RESPONSE,
                    payload={'error':str(err)}
                ),
                logLevel
            )
            return

        if data.kind == DataKindEnum.PING:
            reply = CanalResponseData(
                kind=DataKindEnum.PING,
                response=CanalResponseData.SUCCESS_RESPONSE
            )
        else:
            reply = self._routeMessage(data)

        if not reply:
            reply = CanalResponseData(
                kind=DataKindEnum.GENERAL,
                error=DataErrorEnum.UNRECOGNIZED_REQUEST,
                response=CanalResponseData.FAILED_RESPONSE
            )

        self._sendResponse(reply, logLevel)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _logData
    def _logData(self, data, logLevel):
        if logLevel > 1:
            data.echo(verbose=True, pretty=True)
        elif logLevel > 0:
            data.echo(pretty=True)

#___________________________________________________________________________________________________ _sendResponse
    def _sendResponse(self, response, logLevel):
        self._logData(response, logLevel)
        self.send(response.serialize() + '\n')

#___________________________________________________________________________________________________ _routeMessage
    def _routeMessage(self, data):
        return None

#___________________________________________________________________________________________________ _parseData
    def _parseData(self, message, logLevel):
        cd = CanalData.fromMessage(message)
        self._logData(cd, logLevel)
        return cd


