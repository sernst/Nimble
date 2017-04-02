import nimble
from nimble.mayan.scripts.render import RenderScene


def render(self, directory=None, name=None, flags=None):
    """
    Renders the current scene and saves the result to an image file
    """

    conn = nimble.getConnection()

    return conn.runPythonModule(
        RenderScene,
        name=name,
        directory=directory,
        render_flags=flags
    )
