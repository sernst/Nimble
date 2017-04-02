import os
import tempfile
from nimble import cmds


def run(name='render', directory='~', render_flags=None):
    """ """

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

    return os.path.join(render_directory, '{}.png'.format(name))
