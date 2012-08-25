# ImportedCommand.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

#___________________________________________________________________________________________________ ImportedCommand
class ImportedCommand(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, target, module =None, method =None, **kwargs):
        """Creates a new instance of ImportedCommand."""
        self._target = target
        self._module = module
        self._method = method

        if 'constructorArgs' in kwargs:
            self._constructorArgs = kwargs['constructorArgs']
        else:
            self._constructorArgs = None

        if 'constructorKwargs' in kwargs:
            self._constructorKwargs = kwargs['constructorKwargs']
        else:
            self._constructorKwargs = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: target
    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, value):
        self._target = value

#___________________________________________________________________________________________________ GS: module
    @property
    def module(self):
        return self._module
    @module.setter
    def module(self, value):
        self._module = value

#___________________________________________________________________________________________________ GS: method
    @property
    def method(self):
        return self._method
    @method.setter
    def method(self, value):
        self._method = value

#___________________________________________________________________________________________________ GS: constructorArgs
    @property
    def constructorArgs(self):
        return self._constructorArgs
    @constructorArgs.setter
    def constructorArgs(self, value):
        self._constructorArgs = value

#___________________________________________________________________________________________________ GS: constructorKwargs
    @property
    def constructorKwargs(self):
        return self._constructorKwargs
    @constructorKwargs.setter
    def constructorKwargs(self, value):
        self._constructorKwargs = value

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ toDict
    def toDict(self):
        """Doc..."""

        d = {'target':self._target}
        if self._module:
            d['module'] = self._module
        if self._method:
            d['method'] = self._method
        if self._constructorArgs:
            d['constructorArgs'] = self._constructorArgs
        if self._constructorKwargs:
            d['constructorKwargs'] = self._constructorKwargs

        return d

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
        return '<%s - %s>' % (
            self.__class__.__name__,
            str(self._target) + (('.' + str(self._method)) if self._method else '')
        )
