# DictUtils.py
# Vizme, Inc. (C)2012
# Scott Ernst

import sys

#___________________________________________________________________________________________________ DictUtils
class DictUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ cleanDictKeys
    @classmethod
    def cleanDictKeys(cls, source):
        """ Python 2.6 and below don't allow unicode argument keys, so these must be converted to
            byte strings explicitly to prevent exceptions.
        """

        vi = sys.version_info
        if vi[1] < 7 and vi[0] < 3:
            out = dict()
            for n,v in source.iteritems():
                out[str(n)] = v
        else:
            out = source

        return out

#___________________________________________________________________________________________________ compare
    @classmethod
    def compare(cls, a, b):
        if a is None or b is None:
            return False

        if len(a.keys()) != len(b.keys()):
            return False

        for name, values in a.iteritems():
            if name not in b:
                return False

            # Compare dict values
            if isinstance(value, dict):
                if isinstance(b[name], dict):
                    if not cls.compare(value, b[name]):
                        return False

            # Compare list and tuples
            if isinstance(value, list) or isinstance(value, tuple):
                from vmi.util.list.ListUtils import ListUtils
                if not ListUtils.compare(value, b[name]):
                    return False

            if value != b[name]:
                return False

        return True
