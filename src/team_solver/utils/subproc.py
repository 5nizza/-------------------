"""
Based on:
An example on how to communicate with a subprocess.

Written by Marcus Cavanaugh.
See http://groups.google.com/group/gevent/browse_thread/thread/7fca7230db0509f6
where it was first posted.
"""

import subprocess
import fcntl
import sys
import errno
import os
import gevent
import gevent.socket

def read_pipe(pipe):
    """ pre: pipe is non-blocking """
    chunks = []
    while True:
        try:
            chunk = pipe.read(4096)
            if not chunk:
                break
            chunks.append(chunk)
        except IOError, ex:
            if ex[0] != errno.EAGAIN:
                raise
            sys.exc_clear()
        gevent.socket.wait_read(pipe.fileno())
    return ''.join(chunks)

def write_pipe(pipe, data):
    """ pre: pipe is non-blocking """
    bytes_total = len(data)
    bytes_written = 0
    while bytes_written < bytes_total:
        try:
            # p.stdin.write() doesn't return anything, so use os.write.
            bytes_written += os.write(pipe.fileno(), data[bytes_written:])
        except IOError, ex:
            if ex[0] != errno.EAGAIN:
                raise
            sys.exc_clear()
        gevent.socket.wait_write(pipe.fileno())

#TODO: strange thing: if main thread dies => this func return empty out
def popen_communicate(args, data=''):
    """Communicate with the process non-blockingly.
    
    Returns (return_code, stdout, stderr)
    Exceptions: OSError, IOError
    """
    p = None
    try:
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        fcntl.fcntl(p.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(p.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(p.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

        write_pipe(p.stdin, data)
        p.stdin.close()

        out = read_pipe(p.stdout)
        p.stdout.close()

        err = read_pipe(p.stderr)
        p.stderr.close()

        while p.poll() is None:
            gevent.sleep(0.001) #switch to other greenlet, TODO: 1: find other ways to do async wait in gevent

        return p.returncode, out, err
    finally:
        if p is not None:
            try:
                p.terminate()
                p.wait() #otherwise - zombie!
            except OSError, e:
                if e.errno != errno.ESRCH: #process doesn't exist
                    raise

