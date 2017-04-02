# NimbleResponseData.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble.data.NimbleData import NimbleData


class NimbleResponseData(NimbleData):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    SUCCESS_RESPONSE = 'success'
    FAILED_RESPONSE  = 'failed'


    def __init__(self, **kwargs):
        """Creates a new instance of NimbleResponseData."""
        NimbleData.__init__(self, **kwargs)

        self.response = kwargs.get('response', NimbleResponseData.SUCCESS_RESPONSE)
        self.error    = kwargs.get('error', None)
        self.warnings = kwargs.get('warnings', None)

#===================================================================================================
#                                                                                   G E T / S E T


    @property
    def result(self):
        try:
            return self._payload.get('result')
        except Exception:
            return None


    @property
    def success(self):
        return self.response == NimbleResponseData.SUCCESS_RESPONSE

#===================================================================================================
#                                                                               P R O T E C T E D


    def _createMessage(self):
        """Doc..."""
        d = NimbleData._createMessage(self)
        d['response'] = self.response

        if self.error:
            d['error'] = self.error

        if self.warnings:
            d['warnings'] = self.warnings

        return d

#===================================================================================================
#                                                                               I N T R I N S I C


    def __str__(self):
        return '<%s::%s>' % (self.__class__.__name__, str(self.kind))
