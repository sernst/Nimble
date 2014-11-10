from __future__ import print_function, absolute_import, unicode_literals, division

import nimble
import random
from nimble import cmds
from nimble import MayaCommandException

count = 0
while count < 100:
    result = cmds.polySphere()
    name   = result[0]

    bcmds = nimble.createCommandsBatch()
    index = 0
    while index < 100:
        bcmds.move(
            2.0*(random.random() - 0.5),
            2.0*(random.random() - 0.5),
            2.0*(random.random() - 0.5),
            name, relative=True)

        bcmds.rotate(
            random.random() - 0.5,
            random.random() - 0.5,
            random.random() - 0.5,
            name, relative=True)

        bcmds.scale(
            1.0 + 0.01*(random.random() - 0.5),
            1.0 + 0.01*(random.random() - 0.5),
            1.0 + 0.01*(random.random() - 0.5),
            name, relative=True)

        index += 1

    try:
        bcmds.sendCommandBatch()
    except MayaCommandException as err:
        print('ERROR: Test failed')
        print(err)
        raise

    count += 1

print('Test complete')

