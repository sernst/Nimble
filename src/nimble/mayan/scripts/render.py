from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import tempfile

from nimble import NimbleScriptBase
from nimble import cmds


class RenderScene(NimbleScriptBase):

    def __init__(self):
        NimbleScriptBase.__init__(self)

    def run(self):
        """ """

        name = self.fetch('name', 'remder')
        directory = self.fetch('directory', '~')
        render_flags = self.fetch('render_flags')

        render_directory = os.path.realpath(directory)
        if not os.path.exists(render_directory):
            os.makedirs(render_directory)

        fd, path = tempfile.mkstemp('nimble-render-save-')
        os.close(fd)

        cmds.file(rename=path)
        cmds.file(force=True, save=True, type='mayaBinary')

        flags = ' '.join(render_flags if render_flags else [])
        os.system(' '.join([
            'Render',
            '-r sw',  # software renderer
            '-rd "{}"'.format(render_directory),
            '-of png',
            '-im "{}"'.format(name),
            flags,
            path
        ]))

        try:
            os.remove(path)
        except Exception:
            pass

        self.put('path', os.path.join(render_directory, '{}.png'.format(name)))
