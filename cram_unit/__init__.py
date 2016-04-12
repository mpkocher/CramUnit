VERSION = (0, 8, 1)


def get_version():
    return ".".join([str(i) for i in VERSION])

__version__ = get_version()
