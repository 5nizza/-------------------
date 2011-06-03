'''
Created on May 24, 2011

@author: art_haali
'''
import unittest

import gevent
import gevent.socket

import team_solver.main

from team_solver.cmd_channels.team_solver_messages_pb2 import ReplyMessage

import common
import utils.all

import signal

import random

#TODO: ah: need to setup solvers paths
class Test(unittest.TestCase):
    def server_func(self, port):
        stp_args = "/home/art_haali/projects/stp-fast-prover/trunk/stp/output/bin/stp --SMTLIB2 -p"
        team_solver.main.main(['-p', str(port), '-stp', stp_args, stp_args])
        print 'server_func: exit'
        
    def client_func(self, port, number_of_queries=1, random_close=False):
        sock = gevent.socket.socket()
        sock.connect(('localhost', port))
        for _ in range(1, number_of_queries):
            id = common.send_new_query(sock, common.SAT_QUERY)
            if random_close and random.random() > 1/2.:
                sock.close()
                return
            common.send_cancel_query(sock, id)
            id = common.send_new_query(sock, common.SAT_QUERY)

            reply = None
            while True:
                reply = ReplyMessage()
                common.recv_to_message(sock, reply)
                if reply.cmdId == id:
                    break
            assert reply.type == ReplyMessage.SAT
            common.assert_sat_assignments(reply.sat.assignment, common.SAT_QUERY_ASSIGNMENT)
        sock.close()

    def test_should_work(self):
        port = 18982
        server_g = gevent.spawn(self.server_func, port)
        gevent.sleep(1) #ensure server starts
        self.client_func(port)
        team_solver.main.sigint_handler()
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

        team_solver.main.sigint_handler()
        server_g.join()

    def test_stress_test(self): #TODO: ah, FATAL: blinking test: too many open files
        port = 18982
        server_g = gevent.spawn(self.server_func, port)
        gevent.sleep(1) #ensure server starts

        greenlets = []
        for _ in range(1, 200):
            g = gevent.spawn(self.client_func, port, 3, True)
            greenlets.append(g)
        gevent.joinall(greenlets)
        
        team_solver.main.sigint_handler()
        server_g.join()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_should_work']
    unittest.main()
