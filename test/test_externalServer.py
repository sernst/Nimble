# test_externalServer.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

import time
import canal

canal.startCanal()
canal.echoServerStatus()

from canal.CanalEnvironment import CanalEnvironment
print 'IN MAYA:', CanalEnvironment.inMaya()

time.sleep(5)

canal.stopCanal()

print 'Test complete'

