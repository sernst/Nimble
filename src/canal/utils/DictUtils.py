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


