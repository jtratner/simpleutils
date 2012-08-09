"""
File handling utilities.

"""

from simpletime import pretty_time
def make_filename(filename=None,ext='', prefix='', name_gen=pretty_time,
        append_time = False):
    if filename is None: 
        if append_time and name_gen is pretty_time:
            filename = ''
        else:
            filename = name_gen()
    if append_time:
        filename = filename + pretty_time()
    return prefix+filename+ext

def get_fileobject(filename, mode, ext, prefix=''):
    """ returns a fileobject for given input.

    :param filename: path - str to a path on system
        fileobject - in which case just returned
        ``None`` - uses :func:`~.simpletime.prettytime` to make
    :param str mode: - mode for open
    :param str ext: - added to end of filename
    :param str prefix: added to start of filename

    """
    # if it's a string, get the path
    if isinstance(filename,str):
        f = open(filename,mode)
    # if it is not None, assume it's a file object
    elif filename is not None:
        f = filename
    # otherwise just use default
    else:
        filename = make_filename(filename=filename, ext=ext, prefix=prefix)
        f = open(filename,mode)
    return f
