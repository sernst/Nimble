# NimbleData.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import zlib
import json

from pyaid.dict.DictUtils import DictUtils
from pyaid.string.StringUtils import StringUtils

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.data.enum.DataKindEnum import DataKindEnum



class NimbleData(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _NEWLINE_ESCAPE = '##NEWLINE##'


    def __init__(self, kind =None, payload =None, **kwargs):
        """Creates a new instance of NimbleData."""
        self._kind      = kind if kind else DataKindEnum.GENERAL
        self._payload   = payload if payload else dict()

#===================================================================================================
#                                                                                   G E T / S E T


    @property
    def kind(self):
        return self._kind
    @kind.setter
    def kind(self, value):
        self._kind = value


    @property
    def payload(self):
        return self._payload

#===================================================================================================
#                                                                                     P U B L I C


    def echo(self, verbose =False, pretty =False):
        msg = self._createMessage()
        header = 'RESPONSE' if hasattr(self, 'response') else 'REQUEST'

        if verbose:
            if pretty:
                s = '\n' + 100*'-' + '\n' + header + ':\n' + (len(header) + 1)*'-' + '\n'
                for n,v in DictUtils.iter(msg):
                    s += '   ' + str(n).upper() + ': ' + str(v) + '\n'
                return s
            return header + ': ' + str(msg)

        return '<NIMBLE %s | %s>' % (header, self.kind)


    def serialize(self):
        """Doc..."""
        out = json.dumps(self._createMessage()) \
            .replace('\r','').replace('\n', NimbleData._NEWLINE_ESCAPE).strip()
        if NimbleEnvironment.ENABLE_COMPRESSION:
            out = zlib.compress(out, 6)
            print(out)
            return out
        return out


    @classmethod
    def fromMessage(cls, message):
        if not message:
            return None

        try:
            if NimbleEnvironment.ENABLE_COMPRESSION:
                message = zlib.decompress(message)
            data = json.loads(message.replace(NimbleData._NEWLINE_ESCAPE, '\n').strip())
        except Exception as err:
            print('Corrupt Nimble Data:')
            print(str(message))
            print(err)
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
        except Exception as err:
            print('Invalid Nimble data:')
            print('ERROR: ', err)
            print('MESSAGE:', message)
            print('DATA:', data)
            print('CLASS:', className)
            print('MODULE:', module)

        return None

#===================================================================================================
#                                                                               P R O T E C T E D


    def _createMessage(self):
        """Doc..."""
        return {
            'class':self.__class__.__name__,
            'kind':self.kind,
            'payload':self.payload }

#===================================================================================================
#                                                                               I N T R I N S I C


    def __repr__(self):
        return self.__str__()


    def __unicode__(self):
        return StringUtils.toStr2(self.__str__())


    def __str__(self):
        return '<%s::%s>' % (self.__class__.__name__, str(self.kind))
