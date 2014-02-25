# test_ping.py
# (C)2013-2014
# Scott Ernst

""" This ping tests the basic communication functionality of Nimble in a series of tests that
    exercise call and response behaviors of different types. """

from profilehooks import profile

# Whether or not to echo results for display
runSilent  = True
keepAlive  = True
iterations = 1000

#___________________________________________________________________________________________________ pingTest
@profile
def pingTest():

    from pyaid.string.StringUtils import StringUtils

    import nimble

    nimble.changeKeepAlive(keepAlive)

    conn = nimble.getConnection()

    #-----------------------------------------------------------------------------------------------
    # PING
    #       An empty call that tests that the Nimble connection is able to complete a request and
    #       response loop and prints the response object when complete.
    for i in range(iterations):
        result = conn.ping()
        if not runSilent:
            print u'PING:', result.echo(True, True)

    #-----------------------------------------------------------------------------------------------
    # ECHO
    #       A basic call that sends an echo message, which the remote Nimble server returns in the
    #       response. Confirms that data can be set, read, and returned through the Nimble
    #       connection.
    smallMessage = 'This is a test'
    for i in range(iterations):
        result = conn.echo(smallMessage)
        if not runSilent:
            print u'ECHO:', result.echo(True, True)

    #-----------------------------------------------------------------------------------------------
    # LONG ECHO
    #       A repeat of the echo test, but with a very long echo message that tests the ability for
    #       the Nimble socket protocols to chunk and stream large messages without losing data. The
    #       test is also repeated numerous times to confirm that the nimble socket connection
    #       survives through high-intensity multi-stage communication.
    largeMessage = StringUtils.getRandomString(64000)
    for i in range(iterations):
        result = conn.echo(largeMessage)
        if not runSilent:
            print u'LARGE ECHO[#%s]:' % i, result.echo(True, True)

    print u'\nTests Complete'

pingTest()
