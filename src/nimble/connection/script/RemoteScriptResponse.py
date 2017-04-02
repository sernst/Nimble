# RemoteScriptResponse.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division
from pyaid.dict.DictUtils import DictUtils

from nimble.NimbleEnvironment import NimbleEnvironment


class RemoteScriptResponse(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, scriptGlobalVars =None):
        """Creates a new instance of RemoteScriptResponse."""
        self._result = None
        self._success = True
        self._scriptGlobalVars = scriptGlobalVars

#===================================================================================================
#                                                                                   G E T / S E T


    @property
    def success(self):
        return self._success


    @property
    def result(self):
        if self._scriptGlobalVars:
            if NimbleEnvironment.REMOTE_RESULT_KEY in self._scriptGlobalVars:
                return self._scriptGlobalVars.get(NimbleEnvironment.REMOTE_RESULT_KEY)

        if self._result is None:
            self._result = dict()
        return self._result

#===================================================================================================
#                                                                                     P U B L I C


    def remove(self, key):
        """ Remove the specified key if it exists. """
        if key in self.result:
            del self.result[key]


    def fetch(self, key, defaultValue =None):
        """ Fetches the specified key if it exists and is not None, or returns the defaultValue
            otherwise. """
        return self.result.get(key, defaultValue)


    def put(self, key, value):
        """ Adds the specified key-value pair to the response """
        if value is None:
            self.remove(key)
        else:
            self.result[key] = value


    def puts(self, **kwargs):
        for key, value in DictUtils.iter(kwargs):
            self.put(key, value)


    def addWarning(self, message):
        if message is None:
            return

        if NimbleEnvironment.REMOTE_RESULT_WARNING_KEY not in self.result:
            self.result[NimbleEnvironment.REMOTE_RESULT_WARNING_KEY] = []
        self.result[NimbleEnvironment.REMOTE_RESULT_WARNING_KEY].append(message)


    def putError(self, message):
        if message is None:
            self._success = True
            if NimbleEnvironment.REMOTE_RESULT_ERROR_KEY in self.result:
                del self.result[NimbleEnvironment.REMOTE_RESULT_ERROR_KEY]
            return

        self._success = False
        self.result[NimbleEnvironment.REMOTE_RESULT_ERROR_KEY] = message

#===================================================================================================
#                                                                               I N T R I N S I C


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return '<%s>' % self.__class__.__name__
