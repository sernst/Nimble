# CustomCommandLink.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import functools


class CustomCommandLink(object):
    """ Wraps the remote nimble scripts in the specified package in a dot-syntax callable format
        that can be used transparently on either side of a nimble bridge. """

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self, connection, rootPackage =None):
        """Creates a new instance of CustomCommandLink."""

        if rootPackage is None:
            rootPackage = u'nimble.mayan.scripts'

        self._connection = connection
        self.rootPackage = rootPackage

#===================================================================================================
#                                                                               I N T R I N S I C


    def __call__(self, *args, **kwargs):
        if not args:
            return self

        return CustomCommandLink(
            connection=self._connection,
            rootPackage=self.rootPackage + u'.' + args[0])


    def __getitem__(self, item):
        return self.__call__(item)


    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError

        func = self._connection.runPythonImport
        out = functools.partial(func, self.rootPackage + u'.' + item, className=item)
        return out


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return '<%s>' % self.__class__.__name__
