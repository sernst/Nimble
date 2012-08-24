# MayaRouter.py
# (C)2012 http://www.threeaddone.com
# Scott Ernst


import maya.cmds as mc
import maya.utils as mu

from canal.connection.router.CanalRouter import CanalRouter
from canal.data.CanalResponseData import CanalResponseData
from canal.data.enum.DataErrorEnum import DataErrorEnum
from canal.data.enum.DataKindEnum import DataKindEnum
from canal.utils.DictUtils import DictUtils

#___________________________________________________________________________________________________ MayaRouter
class MayaRouter(CanalRouter):
    """A class for..."""

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _routeMessage
    def _routeMessage(self, data):

        if data.kind == DataKindEnum.MAYA_COMMAND:
            result = mu.executeInMainThreadWithResult(self._executeMayaCommand, data.payload)
            if isinstance(result, CanalResponseData):
                return result
            return CanalResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                response=CanalResponseData.SUCCESS_RESPONSE,
                payload={'result':result}
            )

        return None

#___________________________________________________________________________________________________ _executeMayaCommand
    def _executeMayaCommand(self, payload):
        cmd = getattr(mc, str(payload['command']), None)
        if cmd is None:
            return CanalResponseData(
                kind=DataKindEnum.MAYA_COMMAND,
                error=DataErrorEnum.UNRECOGNIZED_MAYA_COMMAND,
                response=CanalResponseData.FAILED_RESPONSE
            )

        return cmd(
            *payload['args'],
            **DictUtils.cleanDictKeys(payload['kwargs'])
        )

