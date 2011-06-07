'''
Created on May 24, 2011

@author: art_haali
'''
import unittest

import gevent
import gevent.socket

import team_solver.run_server

from team_solver.cmd_channels.team_solver_messages_pb2 import ReplyMessage

import common
import team_solver.utils.all

import signal

import random

#TODO: 1: ah: need to setup solvers paths
class Test(unittest.TestCase):
    def server_func(self, port, num_solvers=2, server_args = []):
        stp_args = common.STP_PATH + " --SMTLIB2 -p"
        solvers = []
        for _ in range(0, num_solvers):
            solvers.append(stp_args)
        team_solver.run_server.main(['-p', str(port)] + server_args + ['-stp'] + solvers)
        print 'server_func: exit'

    def client_func(self, port, number_of_queries=1, random_close=False):
        sock = gevent.socket.socket()
        sock.connect(('127.0.0.1', port))
        for _ in range(1, number_of_queries):
            id = common.send_new_query(sock, common.SAT_QUERY)
            if random_close and random.random() > 1/2.:
                break
            common.send_cancel_query(sock, id)
            id = common.send_new_query(sock, common.SAT_QUERY)

            reply = None
            while True:
                reply = ReplyMessage()
                common.recv_to_message(sock, reply)
                if reply.cmdId == id: #there might be outdated messages
                    break
            assert reply.type == ReplyMessage.SAT
            common.assert_sat_ser_assignments(reply.sat.assignment, common.SAT_QUERY_ASSIGNMENT_SERIALIZED)
        sock.close()

    def test_should_work(self):
        port = 18982
        server_g = gevent.spawn(self.server_func, port)
        gevent.sleep(1) #ensure server starts
        self.client_func(port)
        team_solver.run_server.sigint_handler()
        server_g.join()

    def test_new_cancel_new_cancel(self):
        port = 18982
        server_g = gevent.spawn(self.server_func, port)
        gevent.sleep(1) #ensure server starts

        sock = gevent.socket.socket()
        sock.connect(('localhost', port))

        id = common.send_new_query(sock, common.SAT_QUERY)
        common.send_cancel_query(sock, id)

        id = common.send_new_query(sock, common.SAT_QUERY)
        common.send_cancel_query(sock, id)

        team_solver.run_server.sigint_handler()
        server_g.join()
        
    def test_stress_portfolio(self):
        port = 18982
        server_g = gevent.spawn(self.server_func, port, 10)
        gevent.sleep(1) #TODO: ah, ensure server starts - get rid of

        greenlets = []
        for _ in range(1, 100):
            g = gevent.spawn(self.client_func, port, 10, True)
            greenlets.append(g)
        gevent.joinall(greenlets)

        team_solver.run_server.sigint_handler()
        server_g.join()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_should_work']
    unittest.main()

