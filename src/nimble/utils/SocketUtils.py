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
        socket.sendall(serialData + NimbleEnvironment.TERMINATION_IDENTIFIER)

#___________________________________________________________________________________________________ receiveInChunks
    @classmethod
    def receiveInChunks(cls, socket, chunkSize =None, echo =False):
        if chunkSize is None:
            chunkSize = NimbleEnvironment.SOCKET_CHUNK_SIZE
        chunkSize *= 2

        message = []
        while True:
            try:
                result = socket.recv(chunkSize)
                if result.endswith(NimbleEnvironment.TERMINATION_IDENTIFIER):
                    result = result[:-len(NimbleEnvironment.TERMINATION_IDENTIFIER)]
                    message.append(result)
                    break

                message.append(result)

            except Exception, err:
                if message[-1].endswith(NimbleEnvironment.TERMINATION_IDENTIFIER):
                    message[-1] = message[-1][:-len(NimbleEnvironment.TERMINATION_IDENTIFIER)]
                    break

        if not message:
            return None

        return u''.join(message)
