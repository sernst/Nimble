# test_externalServer.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import time
import nimble

nimble.startServer()
nimble.echoServerStatus()

from nimble.NimbleEnvironment import NimbleEnvironment
print('IN MAYA:', NimbleEnvironment.inMaya())

time.sleep(5)

nimble.stopServer()

print('Test complete')

