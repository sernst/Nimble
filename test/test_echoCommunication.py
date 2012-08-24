# test_echoCommunication.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

import canal

conn = canal.getConnection()
res  = conn.ping('This is a test.')

print 'Connection complete.'
print 'Result:', res
