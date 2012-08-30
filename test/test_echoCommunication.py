# test_echoCommunication.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import nimble

print 100*'-' + '\n', 'TESTING CONNECTION [PING]:'
conn = nimble.getConnection()
print conn.ping('This is a test.')

print 100*'-' + '\n', 'TESTING LONG REQUEST:'
conn = nimble.getConnection()
message = 100*'a' + '\n'
print conn.ping(10*message)

print 100*'-' + '\n', 'TESTING LONG RESPONSE:'
print nimble.cmds.ls()

