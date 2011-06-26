"""
Created on May 13, 2011

@author: art_haali
"""

from sys import stderr
from gevent.timeout import Timeout

from team_solver.interfaces.interfaces import ICmdChannel
from team_solver.interfaces.interfaces import UniqueQuery
from team_solver_messages_pb2  import CommandMessage
from team_solver_messages_pb2 import ReplyMessage

from gevent.server import StreamServer
from gevent.socket import socketpair
from google.protobuf.message import DecodeError

import gevent

import traceback

import struct
import socket as origin_socket
import team_solver.utils.all as utils

#Note on socket:
#1. socket.recv: return ''
#2. socket.send: socket.error is raised

class TcpCmdChannel(ICmdChannel):
    LOG_PREFIX = 'TcpCmdChannel: '
    def __init__(self, local_address, local_port, cmd_handler = None):
        self._cmd_handler = cmd_handler
        self._stream_server = StreamServer((local_address, local_port), self._accept, spawn = self._spawn_hook)
        self._stop = False
        self._ev_stop_getter, self._ev_stop_setter = socketpair()
        self._acceptors = []
        self._queries = {}
        self._socks = {}

    def __enter__(self):
        self.start()
        return self

    #noinspection PyUnusedLocal
    def __exit__(self, type, value, traceback):
        ok = self.stop()
        assert ok

#------------------------------------------------------------------------------
    def _spawn_hook(self, cmd, search_path=1, verbose=0):
        g = gevent.spawn(cmd, search_path, verbose)
        self._acceptors.append(g)
        return g

#------------------------------------------------------------------------------
    def register_cmd_handler(self, cmd_handler): #REFACTOR: think how to remove
        self._cmd_handler = cmd_handler

    def start(self):
        assert self._cmd_handler is not None
        assert self._stop == False
        self._stream_server.start()
        print self.LOG_PREFIX, "started on {0}".format(self._stream_server.address)

    def stop(self):
        self._stop = True
        self._stream_server.stop()
        self._ev_stop_setter.send("game over")
        try:
            with Timeout(2):
                gevent.greenlet.joinall(self._acceptors)
        except Timeout:
            return False
        assert len(self._acceptors) == 0, len(self._acceptors)
        return True

    def send_result(self, solver_result):
        sock = self._get_sock(solver_result.unique_query)
        if sock is not None:
            reply_message = self._create_message(solver_result)
            self._del_query(solver_result.unique_query)
            self._send_message(reply_message, sock)

        #Otherwise the socket was closed and the solver reported result at the same time.

#------------------------------------------------------------------------------
    def _accept(self, socket, address):
        log_prefix = 'client acceptor ({0}): '.format(address)
        print log_prefix, 'started'
        try:
            while True:
                message = self._read_message(socket)
                if self._stop:
                    break
                if message is None: #client disconnected
                    self._cancel_query_on_socket(socket)
                    break

                if message.type == CommandMessage.NEW_QUERY:
                    self._new_query_on_socket(message.cmdId, message.newQuery.query, socket)
                elif message.type == CommandMessage.CANCEL_QUERY:
                    self._cancel_query_on_socket(socket)
                else:
                    assert 0
        except IOError, e:
            print >>stderr, log_prefix, "IO error:\n{0}".format(e)
            self._cancel_query_on_socket(socket)
        except Exception, e:
            print >>stderr, log_prefix, "FATAL error:{0}\n".format(e)
            raise
        finally:
            try:
                socket.close()
            except Exception, e:
                print log_prefix, e
            print log_prefix, "exited"
            self._acceptors.remove(gevent.greenlet.getcurrent())

    def _cancel_query_on_socket(self, sock):
        uniq_query = self._get_query(sock)
        if uniq_query is not None:
            self._del_query(uniq_query)
            self._cmd_handler.on_cancel_query(uniq_query)

    def _new_query_on_socket(self, cmdId, query, sock):
        uniq_query = UniqueQuery(cmdId, query)
        assert self._get_query(sock) is None, 'one active query per client at a time'
        
        self._add_query(uniq_query, sock)
        self._cmd_handler.on_new_query(uniq_query)

#------------------------------------------------------------------------------
    def _read_message(self, socket):
        """ Exceptions: IOError """
        try:
            size_as_raw_string = utils.recv_size(socket, 4, self._ev_stop_getter)

            if self._stop:
                return None
            if size_as_raw_string == '':
                return None

            size_as_uint = long(struct.unpack('I', size_as_raw_string)[0])
            message_as_raw_string = utils.recv_size(socket, size_as_uint, self._ev_stop_getter)

            if self._stop:
                return None
            if message_as_raw_string == '': 
                return None

            result = CommandMessage()
            result.ParseFromString(message_as_raw_string)
            return result

        except ValueError, e:
            raise utils.wrap_exc(IOError, "can't parse a length of a packet", e)
        except DecodeError, e:
            raise utils.wrap_exc(IOError, "can't parse protobuf message", e)
        except origin_socket.error, e:
            raise utils.wrap_exc(IOError, "socket reading error", e)

    def _send_message(self, message, sock):
        message_as_string = message.SerializeToString()
        header = struct.pack('I', len(message_as_string))
        assert len(header) == 4
        try:
            sock.sendall(header)
            sock.sendall(message_as_string)
        except origin_socket.error:
            print traceback.format_exc()

    #noinspection PyUnresolvedReferences
    def _create_message(self, solver_result):
        reply_message = ReplyMessage()
        reply_message.cmdId = solver_result.unique_query.cmd_id
        reply_message.stats.extend(self._serialize_stats(solver_result.stats))
        if solver_result.is_sat:
            reply_message.type = ReplyMessage.SAT #@UndefinedVariable
            reply_message.sat.assignment.extend(self._serialize_assignment(solver_result.assignment))
        else:
            reply_message.type = ReplyMessage.UNSAT #@UndefinedVariable
        return reply_message

    def _serialize_stats(self, solver_result_stats):
        serialized = []
        for s in solver_result_stats:
            serialized.append(str(s) + ': ' + solver_result_stats[s])
        return serialized

    def _serialize_assignment(self, solver_result_assignment):
        serialized = []
        for a in solver_result_assignment:
            arr_name = a
            for index in solver_result_assignment[a]:
                serialized.append('{0}[{1}]={2}'.format(arr_name, index, solver_result_assignment[a][index]))
        return serialized

#-----------------------------------------------------------------------------
    def _get_query(self, sock):
        return self._queries.get(sock)

    def _get_sock(self, query):
        return self._socks.get(query)

    def _del_query(self, query):
        sock = self._socks[query]
        del self._queries[sock]
        del self._socks[query]

    def _add_query(self, query, sock):
        assert sock not in self._queries
        self._queries[sock] = query
        self._socks[query] = sock



        
        
        