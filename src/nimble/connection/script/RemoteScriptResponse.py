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
    def __init__(self, scriptGlobalVars =None):
        """Creates a new instance of RemoteScriptResponse."""
        self._result           = None
        self._scriptGlobalVars = scriptGlobalVars
        self._success          = True

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: success
    @property
    def success(self):
        return self._success

#___________________________________________________________________________________________________ GS: result
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

#___________________________________________________________________________________________________ fetch
    def fetch(self, key, defaultValue =None):
        """Doc..."""
        return self.result.get(key, defaultValue)

#___________________________________________________________________________________________________ put
    def put(self, key, value):
        self.result[key] = value

#___________________________________________________________________________________________________ puts
    def puts(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.result[key] = value

#___________________________________________________________________________________________________ putError
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

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
