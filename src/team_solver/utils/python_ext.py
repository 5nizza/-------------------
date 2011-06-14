def get_index(seq, f):
    """ Return the index of the first item in seq where 'f(item)' evaluates to True
        None otherwise
    """
    #noinspection PyArgumentEqualDefault
    return next((i for i in xrange(len(seq)) if f(seq[i])), None)

def get_val(seq, f):
    """ Return the first item where 'f(item)' evaluates to True
        None otherwise
    """
    for e in seq:
        if f(e):
            return e
    return None