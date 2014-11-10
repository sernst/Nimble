# test_echoCommunication.py
# (C)2012 t
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import nimble
from nimble import cmds

result = cmds.polyCube(height=10, depth=25)
print('polyCube result:',result)
cmds.select(result[0])
cmds.move(10, 10, 5, result[0])

conn = nimble.getConnection()
print(conn.ping().echo(True, True))

print('X:',conn.maya('getAttr', result[0] + '.translateX'))
print('Y:',conn.maya('getAttr', result[0] + '.translateY'))
print('Z:',conn.maya('getAttr', result[0] + '.translateZ'))

print('Translate:', cmds.getAttr(result[0] + '.translate')[0])

print('Test Complete.')
