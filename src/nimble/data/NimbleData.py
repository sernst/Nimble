# NimbleData.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import json

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.data.enum.DataKindEnum import DataKindEnum
from nimble.utils.DictUtils import DictUtils

#___________________________________________________________________________________________________ NimbleData
class NimbleData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _NEWLINE_ESCAPE = '##NEWLINE##'

#___________________________________________________________________________________________________ __init__
    def __init__(self, kind =None, payload =None, **kwargs):
        """Creates a new instance of NimbleData."""
        self._kind      = kind if kind else DataKindEnum.GENERAL
        self._payload   = payload if payload else dict()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: kind
    @property
    def kind(self):
        return self._kind
    @kind.setter
    def kind(self, value):
        self._kind = value

#___________________________________________________________________________________________________ GS: payload
    @property
    def payload(self):
        return self._payload

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ echo
    def echo(self, verbose =False, pretty =False):
        msg    = self._createMessage()
        header = 'RESPONSE' if hasattr(self, 'response') else 'REQUEST'
        if verbose:
            if pretty:
                s = '\n' + 100*'-' + '\n' + header + ':\n' + (len(header) + 1)*'-' + '\n'
                for n,v in msg.iteritems():
                    s += '   ' + str(n).upper() + ': ' + str(v) + '\n'
                NimbleEnvironment.log(s)
            else:
                NimbleEnvironment.log(header + ': ' + str(msg))
        else:
            NimbleEnvironment.log('<NIMBLE %s | %s>' % (header, self.kind))

#___________________________________________________________________________________________________ serialize
    def serialize(self):
        """Doc..."""
        return json.dumps(self._createMessage()) \
            .replace('\r','').replace('\n', NimbleData._NEWLINE_ESCAPE).strip()

#___________________________________________________________________________________________________ fromMessage
    @classmethod
    def fromMessage(cls, message):
        if not message:
            return None

        try:
            data   = json.loads(message.replace(NimbleData._NEWLINE_ESCAPE, '\n').strip())
        except Exception, err:
            print 'Invalid Nimble Data:'
            print str(message)
            print err
            return None

        data      = DictUtils.cleanDictKeys(data)
        className = data['class']
        if className == cls.__name__:
            return NimbleData(**data)

        module = ''
        try:
            module  = '.'.join(cls.__module__.split('.')[:-1]) + '.' + className
            res     = __import__(module, globals(), locals(), [className])
            Source  = getattr(res, className)
            return Source(**data)
        except Exception, err:
            print 'Invalid Nimble data:'
            print 'ERROR: ', err
            print 'MESSAGE:', message
            print 'DATA:', data
            print 'CLASS:', className
            print 'MODULE:', module

        return None

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createMessage
    def _createMessage(self):
        """Doc..."""
        return {
            'class':self.__class__.__name__,
            'kind':self.kind,
            'payload':self.payload
        }

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
        return '<%s::%s>' % (self.__class__.__name__, str(self.kind))
