# SocketUtils.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division
from pyaid.string.StringUtils import StringUtils

from nimble.NimbleEnvironment import NimbleEnvironment


class SocketUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    @classmethod
    def receiveInChunks(cls, socket, chunkSize =None, echo =False):
        if chunkSize is None:
            chunkSize = NimbleEnvironment.SOCKET_CHUNK_SIZE
        chunkSize *= 2

        terminator = StringUtils.unicodeToStr(NimbleEnvironment.TERMINATION_IDENTIFIER)

        message = []
        while True:
            try:
                result = socket.recv(chunkSize)
                if result.endswith(terminator):
                    result = result[:-len(terminator)]
                    message.append(result)
                    break

                message.append(result)

            except Exception as err:
                if not message:
                    print(err)
                    raise

                if message[-1].endswith(terminator):
                    message[-1] = message[-1][:-len(terminator)]
                    break

        if not message:
            return None

        return StringUtils.unicodeToStr('').join(message)
