# test_echoCommunication.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import nimble

conn = nimble.getConnection()
res  = conn.ping('This is a test.')

print 'Connection complete.'
print 'Result:', res
