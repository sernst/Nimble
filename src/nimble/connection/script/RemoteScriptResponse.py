# RemoteScriptResponse.py
# (C)2013
# Scott Ernst

from nimble.NimbleEnvironment import NimbleEnvironment

#___________________________________________________________________________________________________ RemoteScriptResponse
class RemoteScriptResponse(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, scriptGlobalVars):
        """Creates a new instance of RemoteScriptResponse."""
        self._result = None
        self._scriptGlobalVars = scriptGlobalVars

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: result
    @property
    def result(self):
        if NimbleEnvironment.REMOTE_RESULT_KEY in self._scriptGlobalVars:
            return self._scriptGlobalVars.get(NimbleEnvironment.REMOTE_RESULT_KEY)

        if self._result is None:
            self._result = dict()
        return self._result

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ fetch
    def fetch(self, key, defaultValue =None):
        """Doc..."""
        return self.result.get(key, defaultValue)

#___________________________________________________________________________________________________ put
    def put(self, key, value):
        self.result[key] = value

#___________________________________________________________________________________________________ puts
    def puts(self, data):
        for key, value in data.iteritems():
            self.result[key] = value

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
