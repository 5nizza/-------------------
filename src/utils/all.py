'''
Created on May 13, 2011

@author: art_haali
'''

from gevent.event import AsyncResult
import gevent.select
import sys

def arrs_to_assignment(arrs):
    """ #assumption: indexes are sequential 0, .. 
        input: {arr: {index: value}, ..}
    """
    assignment = {} # dict: arr_name -> [] of values
    for a in arrs:
        assignment[a] = []
        for index in range(0, len(arrs[a])): 
            assignment[a].append(arrs[a][index])
    return assignment

def wait_any(events, timeout=None):
    result = AsyncResult()
    update = result.set
    try:
        for event in events:
            if event.ready():
                return event
            else:
                event.rawlink(update)
        return result.get(timeout=timeout)
    finally:
        for event in events:
            event.unlink(update)

def wrap_exc(exception_creater, desc, inner_exc):
    trace = sys.exc_info()[2]
    return exception_creater("{0}: {1}".format(desc, inner_exc)), None, trace

def recv_size(sock, size, cancel_obj = None): #TODO: optimizations: use lengths of ^2, decrease number of generated strings
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



