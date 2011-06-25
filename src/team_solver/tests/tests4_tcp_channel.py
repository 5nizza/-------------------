"""""
Created on May 17, 2011

@author: art_haali
"""""

import unittest
from team_solver.interfaces.interfaces import ICmdHandler
from team_solver.interfaces.interfaces import SolverResult

from team_solver.cmd_channels.tcp_cmd_channel import TcpCmdChannel
from team_solver.cmd_channels.team_solver_messages_pb2 import ReplyMessage

import struct

import gevent
import gevent.socket
from team_solver.tests import common

def _empty(self, uniq_query):
    pass

class Test(unittest.TestCase):

    class CmdHandlerFunc(ICmdHandler):
        def __init__(self, on_new = _empty, on_cancel = _empty):
            self._on_new = on_new
            self._on_cancel = on_cancel
        def _empty(self, uniq_query):
            pass
        def on_new_query(self, uniq_query):
            self._on_new(uniq_query)
        def on_cancel_query(self, uniq_query):
            self._on_cancel(uniq_query)

    class CmdHandler(ICmdHandler):
        def __init__(self, ev_new = gevent.event.Event(), ev_cancel = gevent.event.Event()):
            self._ev_cancel = ev_cancel
            self._ev_new = ev_new
        def on_new_query(self, uniq_query):
            self._ev_new.set()
        def on_cancel_query(self, uniq_query):
            self._ev_cancel.set()
    
    def setUp(self):
        self._accept_original = TcpCmdChannel._accept

    def tearDown(self):
        TcpCmdChannel._accept = self._accept_original

    def test_StartStop(self):
        tcp_cmd_channel = TcpCmdChannel('localhost', 12346)
        tcp_cmd_channel.register_cmd_handler('anything')
        tcp_cmd_channel.start()
        tcp_cmd_channel.stop()
        
    def test_StartStop_many(self):
        for _ in range(1, 10):
            self.test_StartStop()

    def test_CmdHandler(self):
        ev_cancel = gevent.event.Event()
        ev_new = gevent.event.Event()

        with TcpCmdChannel('localhost', 12346, Test.CmdHandler(ev_new, ev_cancel)) as tcp_cmd_channel:
            sock = gevent.socket.socket()
            sock.connect(('localhost', 12346))
            for _ in range(1, 5):
                ev_new.clear()
                ev_cancel.clear()
    
                id = common.send_new_query(sock, common.SAT_QUERY_SMT)
                assert ev_new.wait(5)

                common.send_cancel_query(sock, id)
                assert ev_cancel.wait(5)
                
    def test_Cancel_On_ClientDisconnect(self):
        ev_cancel = gevent.event.Event()
        ev_new = gevent.event.Event()

        with TcpCmdChannel('localhost', 12346, Test.CmdHandler(ev_new, ev_cancel)) as tcp_cmd_channel:
            sock = gevent.socket.socket()
            sock.connect(('localhost', 12346))
            
            common.send_new_query(sock, common.SAT_QUERY_SMT)
            assert ev_new.wait(5)

            sock.close()
            assert ev_cancel.wait(5)

    def test_StopAcceptor(self):
        ev_acceptor_started = gevent.event.Event()
        def accept_hook(self_obj, socket, address):
            ev_acceptor_started.set()
            #noinspection PyArgumentList
            self._accept_original(self_obj, socket, address)
        TcpCmdChannel._accept = accept_hook

        cmd_channel = TcpCmdChannel('localhost', 12346, Test.CmdHandler()) 
        cmd_channel.start()

        sock = gevent.socket.socket()
        sock.connect(('localhost', 12346))
        sock.sendall(struct.pack('I', 1000))

        assert ev_acceptor_started.wait()
        assert cmd_channel.stop()

    def test_StopHangedAcceptor(self):
        ev_accepted = gevent.event.Event()
        def accept_hook(self_obj, socket, address):
            ev_accepted.set()
            gevent.sleep(999)
        TcpCmdChannel._accept = accept_hook

        cmd_channel = TcpCmdChannel('localhost', 12346, Test.CmdHandler())
        cmd_channel.start()

        sock = gevent.socket.socket()
        sock.connect(('localhost', 12346))

        assert ev_accepted.wait()
        assert not cmd_channel.stop()


    def test_SendResult(self):
        self.uniq_query = None
        self.ev_new = gevent.event.Event()
        def on_new(u_q):
            assert u_q is not None
            self.uniq_query = u_q
            self.ev_new.set()
        with TcpCmdChannel('localhost', 12346, Test.CmdHandlerFunc(on_new)) as tcp_cmd_channel:
            assert tcp_cmd_channel is not None
            sock = gevent.socket.socket()
            sock.connect(('localhost', 12346))
            
            common.send_new_query(sock, common.SAT_QUERY_SMT)
            assert self.ev_new.wait(5)
            assert self.uniq_query is not None

            result = SolverResult(self.uniq_query, True, {'some solver': '1212'}, {'arr':[0, 1, 2, 3]})
            assert tcp_cmd_channel is not None
            tcp_cmd_channel.send_result(result)
            common.recv_to_message(sock, ReplyMessage())
            #no exceptions, OK


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNewQueryCmdShouldWork']
    import sys
    print sys.path
    unittest.main()