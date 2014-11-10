# EchoStatus.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble import cmds
from nimble import NimbleScriptBase

#___________________________________________________________________________________________________ EchoStatus
class EchoStatus(NimbleScriptBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of EchoStatus."""
        NimbleScriptBase.__init__(self)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""
        version = cmds.about(version=True)
        print('VERSION:', version)

        buildDate = cmds.about(date=True)
        print('BUILD DATE:', buildDate)

        self.addWarning('Test warning!')
        self.puts(version=version, date=buildDate)
