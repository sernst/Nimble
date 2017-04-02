try:
    # noinspection PyUnresolvedReferences
    import maya.utils as mu
except Exception:
    mu = None

executionFunction = (
    mu.executeInMainThreadWithResult
    if mu is not None else
    None
)


def executeWithResult(function, *args, **kwargs):
    """ """

    if executionFunction is not None:
        return executionFunction(function, *args, **kwargs)

    return function(*args, **kwargs)
