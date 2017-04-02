# MayaEnvEntry.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os

from pyaid.file.FileUtils import FileUtils


class MayaEnvEntry(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, rootName, folderPath):
        """Creates a new instance of MayaEnvEntry."""
        self.rootName   = rootName
        self.folderPath = folderPath

#===================================================================================================
#                                                                                   G E T / S E T


    @property
    def rootPath(self):
        return FileUtils.createPath(self.folderPath, self.rootName, noTail=True)

#===================================================================================================
#                                                                                     P U B L I C


    @classmethod
    def fromRootPath(cls, path):
        """Doc..."""
        parts = path.rsplit(os.sep, 1)
        return MayaEnvEntry(parts[-1], FileUtils.cleanupPath(parts[0], noTail=True))

#===================================================================================================
#                                                                               I N T R I N S I C


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return '<%s>' % self.__class__.__name__
