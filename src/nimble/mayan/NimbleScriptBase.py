# NimbleScriptBase.py
# (C)2014
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger

import nimble
from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.script.RemoteScriptResponse import RemoteScriptResponse

#___________________________________________________________________________________________________ NimbleScriptBase
class NimbleScriptBase(object):
    """ The base class for remote nimble scripts, which transparently handles running scripts both
        inside and outside (across nimble communication bridge) of Maya. """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of NimbleScriptBase."""
        self.kwargs = None
        self.response = None
        self._savedSelection = None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """ The execution method that should be implemented in subclasses to carry out the remote
            script. """
        pass

#___________________________________________________________________________________________________ runAsNimbleScript
    def runAsNimbleScript(self, **kwargs):
        """ Used to call the remote script as an independent operation outside of a MayaRouter, the
            normal method by which the script is executed. Used primarily for unit testing purposes
            and should not be called during normal operation.

            [kwargs]: Script arguments """

        self.kwargs     = kwargs if kwargs else nimble.getRemoteKwargs(globals())
        self.response   = nimble.createRemoteResponse(globals())
        self.run()

#___________________________________________________________________________________________________ fetch
    def fetch(self, name, defaultValue =None):
        """ Retrieves the value of the script argument specified by the name. If no such argument
            exists (or the argument is None) the default value will be returned.

            name: Script argument name to fetch.
            [defaultValue =None]: Value returned if the script argument is None or missing. """
        return ArgsUtils.get(name, defaultValue, self.kwargs)

#___________________________________________________________________________________________________ put
    def put(self, name, value):
        """ Places the specified name-value pair in the response that will be returned at the
            completion of the script execution. Setting the value more than once will overwrite the
            previously assigned value.

            name: Response key to set
            value: Response value to assign the to key. If the value is None the key will be
                removed if the value already exists. """

        self.response.put(name, value)

#___________________________________________________________________________________________________ puts
    def puts(self, **kwargs):
        self.response.puts(**kwargs)

#___________________________________________________________________________________________________ addWarning
    def addWarning(self, message):
        self.response.addWarning(message)

#___________________________________________________________________________________________________ putErrorResult
    def putErrorResult(self, message, **kwargs):
        self.response.putError(message)
        if kwargs:
            self.puts(kwargs)

#___________________________________________________________________________________________________ saveSelection
    def saveSelection(self, override =None, **kwargs):
        if override is None:
            override = nimble.cmds.ls(selection=True, **kwargs)
        self._savedSelection = override

#___________________________________________________________________________________________________ restoreSelection
    def restoreSelection(self, override =None):
        if override is None:
            override = self._savedSelection

        if not override:
            nimble.cmds.select(clear=True)
        else:
            nimble.cmds.select(*override, replace=True)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __call__
    def __call__(self, *args, **kwargs):
        """Doc..."""
        if self.response is None:
            self.response = RemoteScriptResponse()
        if self.kwargs is None:
            self.kwargs = kwargs

        try:
            self.run()
        except Exception, err:
            message = u'Nimble remote script run failure'
            NimbleEnvironment.logError(message, err)
            logMessage = Logger.createErrorMessage(message, err)
            self.putErrorResult(
                Logger.logMessageToString(logMessage=logMessage, includePrefix=False))
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
