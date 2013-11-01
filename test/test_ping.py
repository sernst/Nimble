from pyaid.string.StringUtils import StringUtils

import nimble

conn = nimble.getConnection()

result = conn.ping()
print 'PING:', result.echo(True, True)

result = conn.echo('This is a test')
print 'ECHO:', result.echo(True, True)

largeMessage = StringUtils.getRandomString(64000)
result = conn.echo(largeMessage)
print 'LARGE ECHO:', result.echo(True, True)

print 'Operation complete'
