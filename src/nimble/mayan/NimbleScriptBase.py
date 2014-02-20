# NimbleScriptBase.py
# (C)2014
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

import nimble
from nimble.connection.script.RemoteScriptResponse import RemoteScriptResponse

#___________________________________________________________________________________________________ NimbleScriptBase
class NimbleScriptBase(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of NimbleScriptBase."""
        self.kwargs   = kwargs
        self.response = None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        pass

#___________________________________________________________________________________________________ runAsNimbleScript
    def runAsNimbleScript(self, **kwargs):
        self.kwargs     = kwargs if kwargs else nimble.getRemoteKwargs(globals())
        self.response   = nimble.createRemoteResponse(globals())
        self.run()

#___________________________________________________________________________________________________ getKwarg
    def getKwarg(self, name, defaultValue =None):
        """Doc..."""
        return ArgsUtils.get(name, defaultValue, self.kwargs)

#___________________________________________________________________________________________________ setKwargs
    def setKwargs(self, **kwargs):
        """ For use when not running as a remote script. """
        self.kwargs = kwargs

#___________________________________________________________________________________________________ fetch
    def fetch(self, key, defaultValue =None):
        """ Quick access to fetch response values. """
        return self.response.fetch(key, defaultValue)

#___________________________________________________________________________________________________ put
    def put(self, key, value):
        """ Quick access to put response values. """
        self.response.put(key, value)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, *args, **kwargs):
        """Doc..."""
        if self.response is None:
            self.response = RemoteScriptResponse()
        if self.kwargs is None:
            self.kwargs = kwargs
        self.run()
        result = self.response.result
        return result if result else dict()

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
