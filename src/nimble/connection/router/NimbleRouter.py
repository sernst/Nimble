# NimbleRouter.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

import asyncore

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.data.NimbleData import NimbleData
from nimble.data.NimbleResponseData import NimbleResponseData
from nimble.data.enum.DataErrorEnum import DataErrorEnum
from nimble.data.enum.DataKindEnum import DataKindEnum
from nimble.utils.SocketUtils import SocketUtils

#___________________________________________________________________________________________________ NimbleRouter
class NimbleRouter(asyncore.dispatcher_with_send):

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ handle_read
    def handle_read(self):
        message = SocketUtils.receiveInChunks(self)

        if not message:
            return

        logLevel = NimbleEnvironment.getServerLogLevel()

        try:
            data = self._parseData(message, logLevel)
        except Exception, err:
            self._sendResponse(
                NimbleResponseData(
                    kind=DataKindEnum.GENERAL,
                    error=DataErrorEnum.PARSE_FAILURE,
                    response=NimbleResponseData.FAILED_RESPONSE,
                    payload={'error':str(err)} ),
                logLevel )
            return

        if data.kind == DataKindEnum.PING:
            reply = NimbleResponseData(
                kind=DataKindEnum.PING,
                response=NimbleResponseData.SUCCESS_RESPONSE)
        else:
            reply = self._routeMessage(data)

        if not reply:
            reply = NimbleResponseData(
                kind=DataKindEnum.GENERAL,
                error=DataErrorEnum.UNRECOGNIZED_REQUEST,
                response=NimbleResponseData.FAILED_RESPONSE )

        self._sendResponse(reply, logLevel)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _logData
    def _logData(self, data, logLevel):
        if logLevel == -1:
            return

        # Assume successful for data unless the data object specifies otherwise, which only exists
        # in certain cases
        success = True
        try:
            success = data.success
        except Exception, err:
            pass

        if logLevel > 1 or not success:
            data.echo(verbose=True, pretty=True)
        elif logLevel > 0:
            data.echo(pretty=True)

#___________________________________________________________________________________________________ _sendResponse
    def _sendResponse(self, response, logLevel):
        self._logData(response, logLevel)
        SocketUtils.sendInChunks(self, response.serialize(), chunkSize=200)
        self.close()

#___________________________________________________________________________________________________ _routeMessage
    def _routeMessage(self, data):
        return None

#___________________________________________________________________________________________________ _parseData
    def _parseData(self, message, logLevel):
        cd = NimbleData.fromMessage(message)
        self._logData(cd, logLevel)
        return cd


