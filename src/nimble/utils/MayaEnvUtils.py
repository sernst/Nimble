# MayaEnvUtils.py
# (C)2013-2014
# Scott Ernst

import os
import re
from collections import namedtuple

import pyaid
from pyaid.OsUtils import OsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils

import nimble

import pyglass

#___________________________________________________________________________________________________ MayaEnvUtils
class MayaEnvUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    MAYA_ENV_MODIFIED_RESULT_NT = namedtuple(
        u'MAYA_ENV_MODIFIED_RESULT_NT',
        [u'added', u'removed'])

    _PYTHON_PATH_PATTERN = re.compile('PYTHONPATH=(?P<paths>[^\n\r]+)')

#___________________________________________________________________________________________________ locateMayaEnvFiles
    @classmethod
    def locateMayaEnvFiles(cls):
        """ Finds the location of all Maya.env files located in the default location on the host
            and return them as a list. If no such env files exist, the method returns an empty
            list. """

        documents = FileUtils.cleanupPath(OsUtils.getDocumentsPath(), isDir=True)
        if not os.path.exists(documents):
            return []

        if OsUtils.isWindows():
            root = FileUtils.createPath(documents, 'maya', isDir=True)
            if not os.path.exists(root):
                return []
        elif OsUtils.isMac():
            root = FileUtils.createPath(
                documents, 'Library', 'Preferences', 'Autodesk', 'maya', isDir=True)
            if not os.path.exists(root):
                return []
        else:
            return []

        out = []
        FileUtils.walkPath(root, cls._handleFindEnvFiles, out)
        return out

#___________________________________________________________________________________________________ checkEnvFile
    @classmethod
    def checkEnvFile(cls, target):
        """Doc..."""
        pathSep   = OsUtils.getPerOsValue(u';', u':')
        additions = cls._getSourcePaths()

        with open(target, 'r') as f:
            contents = f.read()

        result = cls._PYTHON_PATH_PATTERN.search(contents)
        if not result:
            return False

        paths = result.groupdict()['paths'].split(pathSep)
        index = 0
        for addition in additions:
            found = False
            for p in paths:
                if p == addition:
                    found = True
                    break
            if not found:
                return False

        return True

#___________________________________________________________________________________________________ modifyEnvFile
    @classmethod
    def modifyEnvFile(cls, target, install =True, test =False):
        """Doc..."""
        pathSep   = OsUtils.getPerOsValue(u';', u':')
        removals  = []
        additions = cls._getSourcePaths()

        with open(target, 'r') as f:
            contents = f.read()

        result = cls._PYTHON_PATH_PATTERN.search(contents)
        if not result:
            if install:
                contents += (u'\n' if contents else u'') + u'PYTHONPATH=' + pathSep.join(additions)
            else:
                return cls.MAYA_ENV_MODIFIED_RESULT_NT([], [])
        else:
            paths = result.groupdict()['paths'].split(pathSep)
            index = 0
            while index < len(paths):
                if not additions:
                    break

                p = paths[index]

                # If path already exists don't add it again
                if p in additions:
                    additions.remove(p)
                    if not install:
                        removals.append(p)
                        paths.remove(p)
                    else:
                        index += 1
                    continue
                elif not install:
                    index += 1
                    continue

                # Remove unrecognized paths that import nimble, pyaid, or pyglass
                testPaths = [
                    FileUtils.createPath(p, u'nimble',  isDir=True),
                    FileUtils.createPath(p, u'pyaid',   isDir=True),
                    FileUtils.createPath(p, u'pyglass', isDir=True) ]
                for test in testPaths:
                    if os.path.exists(test):
                        paths.remove(p)
                        continue

                index += 1

            paths += additions
            contents = contents[:result.start()] + u'PYTHONPATH=' + pathSep.join(paths) \
                + u'\n' + contents[result.end():]

        result = cls.MAYA_ENV_MODIFIED_RESULT_NT(additions if install else [], removals)
        if test:
            return result

        with open(target, 'w') as f:
            f.write(contents)

        return result

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSourcePaths
    @classmethod
    def _getSourcePaths(cls):
        pathSep = OsUtils.getPerOsValue(u';', u':')

        nimblePath = FileUtils.createPath(
            FileUtils.getDirectoryOf(nimble.__file__),
            '..', isDir=True, noTail=True)

        pyaidPath = FileUtils.createPath(
            FileUtils.getDirectoryOf(pyaid.__file__),
            '..', isDir=True, noTail=True)

        pyglassPath = FileUtils.createPath(
            FileUtils.getDirectoryOf(pyglass.__file__),
            '..', isDir=True, noTail=True)

        additions = [nimblePath]
        if not StringUtils.matches(pyaidPath, additions):
            additions.append(pyaidPath)

        if not StringUtils.matches(pyglassPath, additions):
            additions.append(pyglassPath)

        return additions

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleFindEnvFiles
    @classmethod
    def _handleFindEnvFiles(cls, walkData):
        for name in walkData.names:
            if name == u'Maya.env':
                walkData.data.append(FileUtils.createPath(walkData.folder, name))
