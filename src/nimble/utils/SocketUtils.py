# SocketUtils.py
# (C)2013
# Scott Ernst

from nimble.NimbleEnvironment import NimbleEnvironment

#___________________________________________________________________________________________________ SocketUtils
class SocketUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ sendInChunks
    @classmethod
    def sendInChunks(cls, socket, serialData, chunkSize =None):
        if chunkSize is None:
            chunkSize = NimbleEnvironment.SOCKET_CHUNK_SIZE

        serialData  += NimbleEnvironment.TERMINATION_IDENTIFIER
        socket.sendall(serialData)
        #serialLength = len(serialData)
        #offset       = 0
        #while offset < serialLength:
        #    start  = offset
        #    offset = min(serialLength, start + chunkSize)
        #    socket.send(serialData[start:offset])

#___________________________________________________________________________________________________ receiveInChunks
    @classmethod
    def receiveInChunks(cls, socket, chunkSize =None, echo =False):
        if chunkSize is None:
            chunkSize = NimbleEnvironment.SOCKET_CHUNK_SIZE
        chunkSize *= 2

        message = u''
        while True:
            try:
                result   = socket.recv(chunkSize)
                message += result

                if message.endswith(NimbleEnvironment.TERMINATION_IDENTIFIER):
                    message = message[:-len(NimbleEnvironment.TERMINATION_IDENTIFIER)]
                    break

            except Exception, err:
                if message.endswith(NimbleEnvironment.TERMINATION_IDENTIFIER):
                    message = message[:-len(NimbleEnvironment.TERMINATION_IDENTIFIER)]
                    break

        if not message:
            return None

        return message
