# MayaCommandException.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division


class MayaCommandException(Exception):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, *args, **kwargs):
        """Creates a new instance of MayaCommandException."""
        self._responseData = kwargs.get('response') if 'response' in kwargs else None
        Exception.__init__(self, *args)

#===================================================================================================
#                                                                                   G E T / S E T


    @property
    def response(self):
        return self._responseData
    @response.setter
    def response(self, value):
        self._responseData = value

#===================================================================================================
#                                                                                     P U B L I C


    def echo(self, verbose =True, pretty =True):
        """echo doc..."""
        if not self.response:
            return 'No response data'
        return self.response.echo(verbose=verbose, pretty=pretty)
