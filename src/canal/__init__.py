# __init__.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst

import atexit

from canal.CanalEnvironment import CanalEnvironment
from canal.connection.CanalConnection import CanalConnection
from canal.connection.thread.CanalServerThread import CanalServerThread

#===================================================================================================
#                                                                               F U N C T I O N S

#___________________________________________________________________________________________________ startCanal
def startCanal(inMaya =None, router =None, logLevel =0):
    CanalEnvironment.inMaya(override=inMaya)
    CanalEnvironment.setServerLogLevel(logLevel)
    CanalServerThread(router=router).start()

#___________________________________________________________________________________________________ changeServerLogLevel
def changeServerLogLevel(level =0):
    return CanalEnvironment.setServerLogLevel(level)

#___________________________________________________________________________________________________ startCanal
def stopCanal():
    return CanalServerThread.closeServer()

#___________________________________________________________________________________________________ echoServerStatus
def echoServerStatus():
    if CanalServerThread.isActivating():
        print 'Canal server is loading'
        return True

    if CanalServerThread.isRunning():
        print 'Canal server is running.'
        return True

    print 'Canal server is inactive.'
    return False

#___________________________________________________________________________________________________ getConnection
def getConnection(inMaya =None, forceCreate =False, **kwargs):
    CanalEnvironment.inMaya(override=inMaya)
    return CanalConnection.getConnection(forceCreate=forceCreate)

#===================================================================================================
#                                                                                     M O D U L E

cmds = None
if CanalEnvironment.inMaya():
    import maya.cmds as mc
    cmds = mc
else:
    cmds = getConnection().mayaCommands

atexit.register(
    CanalConnection.closeConnectionPool
)
