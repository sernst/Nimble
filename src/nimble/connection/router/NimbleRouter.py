# NimbleRouter.py
# (C)2012-2014
# Scott Ernst

import asynchat

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.data.NimbleData import NimbleData
from nimble.data.NimbleResponseData import NimbleResponseData
from nimble.data.enum.DataErrorEnum import DataErrorEnum
from nimble.data.enum.DataKindEnum import DataKindEnum

#___________________________________________________________________________________________________ NimbleRouter
class NimbleRouter(asynchat.async_chat):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________
    def __init__(self, sock, **kwargs):
        asynchat.async_chat.__init__(self, sock=sock)
        self.set_terminator(NimbleEnvironment.TERMINATION_IDENTIFIER)
        self.ibuffer         = []
        self.obuffer         = u''
        self._message        = None
        self.reading_headers = True
        self.handling        = False

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ collect_incoming_data
    def collect_incoming_data(self, data):
        """Buffer the data"""
        if data:
            self.ibuffer.append(data)

#___________________________________________________________________________________________________ found_terminator
    def found_terminator(self):
        if self.handling:
            return

        self.set_terminator(None) # connections sometimes over-send
        self.handling = True
        self._message = u''.join(self.ibuffer)
        self.handle_request()

#___________________________________________________________________________________________________ handle_read
    def handle_request(self):
        message = self._message
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
        self.obuffer = response.serialize() + NimbleEnvironment.TERMINATION_IDENTIFIER
        self.push(self.obuffer)
        self.close_when_done()

#___________________________________________________________________________________________________ _routeMessage
    def _routeMessage(self, data):
        if data.kind == DataKindEnum.ECHO:
            return NimbleResponseData(
                kind=DataKindEnum.ECHO,
                response=NimbleResponseData.SUCCESS_RESPONSE,
                payload={'echo':data.payload['echo']} )
        else:
            result = self._routeMessageImpl(data)
            if result is not None:
                return result

        return NimbleResponseData(
            kind=DataKindEnum.GENERAL,
            error=DataErrorEnum.UNRECOGNIZED_REQUEST,
            response=NimbleResponseData.FAILED_RESPONSE )

#___________________________________________________________________________________________________
    def _routeMessageImpl(self, data):
        return None

#___________________________________________________________________________________________________ _parseData
    def _parseData(self, message, logLevel):
        cd = NimbleData.fromMessage(message)
        self._logData(cd, logLevel)
        return cd


