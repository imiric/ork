__author__ = 'Ivan Mirić <imiric@gmail.com>'
__version__ = (0, 0, 0)


from .task import task, Task  # NOQA


def get_version():
    return '.'.join(str(bit) for bit in __version__)
