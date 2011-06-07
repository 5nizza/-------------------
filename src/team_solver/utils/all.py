'''
Created on May 13, 2011

@author: art_haali
'''

from gevent.event import AsyncResult
import gevent.select
import sys


def wait_any(gevent_events, timeout=None):
    result = AsyncResult()
    update = result.set
    try:
        for event in gevent_events:
            if event.ready():
                return event
            else:
                event.rawlink(update)
        return result.get(timeout=timeout)
    finally:
        for event in gevent_events:
            event.unlink(update)

def wrap_exc(new_exc_creater, desc, exc_to_wrap):
    """ Return (wrapped exception, None, original trace) """
    trace = sys.exc_info()[2]
    return new_exc_creater("{0}: {1}".format(desc, exc_to_wrap)), None, trace

def recv_size(sock, size, cancel_obj = None): #TODO: optimizations: use lengths of ^2, decrease number of generated strings
    """ Return:
        string of requested size
        or '' in case of EOF
        or None if cancelled
    """
    remained = size
    result = ''
    objects_to_wait = [sock]
    if cancel_obj != None:
        objects_to_wait.append(cancel_obj)
    while remained != 0:
        ready_to_read, _, __ =  gevent.select.select(objects_to_wait, [], [])

        if cancel_obj in ready_to_read:
            return None

        new = sock.recv(remained)
        if new == '':
            return ''
        remained -= len(new)
        result += new
    return result



