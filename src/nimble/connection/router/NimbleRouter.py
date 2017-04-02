# NimbleRouter.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import sys
import time
import asynchat

from pyaid.string.ByteChunk import ByteChunk
from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.data.NimbleData import NimbleData
from nimble.data.NimbleResponseData import NimbleResponseData
from nimble.data.enum.DataErrorEnum import DataErrorEnum
from nimble.data.enum.DataKindEnum import DataKindEnum
from nimble.enum.ConnectionFlags import ConnectionFlags


class NimbleRouter(asynchat.async_chat):

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock)
        self._createTime    = TimeUtils.getNowSeconds()
        self._data          = None
        self._message       = None
        self.handling       = False
        self._requestFlags  = 0
        self._responseFlags = 0
        self._chunk         = ByteChunk(endianess=ByteChunk.BIG_ENDIAN)
        self._resetRouterState()

#===================================================================================================
#                                                                                   G E T / S E T


    @property
    def keepAlive(self):
        return self._requestFlags & ConnectionFlags.KEEP_ALIVE \
            and (TimeUtils.getNowSeconds() - self._createTime < NimbleEnvironment.CONNECTION_LIFETIME)

#===================================================================================================
#                                                                                     P U B L I C


    def collect_incoming_data(self, data):
        """Buffer the data until the terminator is found"""
        if data:
            self._data.append(data)


    def found_terminator(self):
        if self.handling:
            return

        self.set_terminator(None) # connections sometimes over-send
        self.handling = True
        # noinspection PyTypeChecker
        self._chunk.writeString(''.join(self._data))
        self._chunk.position = 0
        self._requestFlags    = self._chunk.readUint32()
        self._message        = StringUtils.strToUnicode(str(self._chunk.read(-1)))
        self.handle_request()


    def handle_request(self):
        message = self._message
        if not message:
            return

        logLevel = NimbleEnvironment.getServerLogLevel()

        try:
            data = self._parseData(message, logLevel)
        except Exception as err:
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


    def _resetRouterState(self):
        self.set_terminator(NimbleEnvironment.TERMINATION_IDENTIFIER)
        self._data          = []
        self._message       = None
        self.handling       = False
        self._responseFlags = 0
        self._chunk.clear()


    # noinspection PyMethodMayBeStatic
    def _logData(self, data, logLevel):
        if logLevel == -1:
            return

        # Assume successful for data unless the data object specifies otherwise, which only exists
        # in certain cases
        success = True
        try:
            success = data.success
        except Exception:
            pass

        if logLevel > 1 or not success:
            NimbleEnvironment.logger.write(data.echo(verbose=True, pretty=True))
        elif logLevel > 0:
            NimbleEnvironment.logger.write(data.echo(pretty=True))


    def _sendResponse(self, responseData, logLevel):
        self._logData(responseData, logLevel)

        flags = self._responseFlags
        if self.keepAlive:
            flags = flags | ConnectionFlags.KEEP_ALIVE

        self._chunk.clear()
        self._chunk.writeUint32(flags)
        self._chunk.writeString(responseData.serialize() + NimbleEnvironment.TERMINATION_IDENTIFIER)
        print('CHUNK:', self._chunk)
        reply     = bytes(self._chunk.byteArray)
        keepAlive = self.keepAlive

        # Clear state for future use before sending response
        self._resetRouterState()

        self.push(reply)

        time.sleep(0.0001)
        if not keepAlive:
            self.close_when_done()


    def _routeMessage(self, data):
        if data.kind == DataKindEnum.ECHO:
            return NimbleResponseData(
                kind=DataKindEnum.ECHO,
                response=NimbleResponseData.SUCCESS_RESPONSE,
                payload={'echo':data.payload['echo']} )
        elif data.kind == DataKindEnum.ADD_SYSTEM_PATH:
            path  = data.payload['path']
            doAdd = path not in sys.path
            if doAdd:
                sys.path.append(path)
            return NimbleResponseData(
                kind=DataKindEnum.ADD_SYSTEM_PATH,
                response=NimbleResponseData.SUCCESS_RESPONSE,
                payload={'added':doAdd} )
        else:
            result = self._routeMessageImpl(data)
            if result is not None:
                return result

        return NimbleResponseData(
            kind=DataKindEnum.GENERAL,
            error=DataErrorEnum.UNRECOGNIZED_REQUEST,
            response=NimbleResponseData.FAILED_RESPONSE )


    def _routeMessageImpl(self, data):
        return None


    def _parseData(self, message, logLevel):
        data = NimbleData.fromMessage(message)
        self._logData(data, logLevel)
        return data
