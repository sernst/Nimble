# CanalResponseData.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

from canal.data.CanalData import CanalData

#___________________________________________________________________________________________________ CanalResponseData
class CanalResponseData(CanalData):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    SUCCESS_RESPONSE = 'success'
    FAILED_RESPONSE  = 'failed'

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of CanalResponseData."""
        CanalData.__init__(self, **kwargs)
        if 'response' in kwargs:
            self._response = kwargs['response']
        else:
            self._response = CanalResponseData.SUCCESS_RESPONSE

        if 'error' in kwargs:
            self._error = kwargs['error']
        else:
            self._error = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: success
    @property
    def success(self):
        return self._response == CanalResponseData.SUCCESS_RESPONSE

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        return self._response
    @response.setter
    def response(self, value):
        self._response = value

#___________________________________________________________________________________________________ GS: error
    @property
    def error(self):
        return self._error
    @error.setter
    def error(self, value):
        self._error = value

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createMessage
    def _createMessage(self):
        """Doc..."""
        d = CanalData._createMessage(self)
        d['response'] = self.response

        if self.error:
            d['error'] = self.error

        return d

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s::%s>' % (self.__class__.__name__, str(self.kind))
