import nimble
from nimble.mayan.scripts.render import RenderScene


def render(directory=None, name=None, flags=None):
    """
    Renders the current scene and saves the result to an image file
    """

    conn = nimble.getConnection()

    return conn.runPythonClass(
        RenderScene,
        name=name,
        directory=directory,
        render_flags=flags
    )
