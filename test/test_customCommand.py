# test_customCommand.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from nimble import scripts

target = scripts('debug').EchoStatus
result = target()
print(result.echo(verbose=True, pretty=True))

target = scripts['transform'].ShrinkToBounds
result = target(x=1.0, y=1.0, z=1.0)
print(result.echo(verbose=True, pretty=True))

print('=== Custom Command Test Complete ===')

