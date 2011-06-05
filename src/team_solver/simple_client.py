#!/usr/bin/env python    
'''
Created on May 27, 2011

@author: art_haali
'''

import sys
import argparse
import tests.common

import gevent.socket

from team_solver.cmd_channels.team_solver_messages_pb2 import ReplyMessage

def main(argv):
    parser = argparse.ArgumentParser(description='Simple client to SMT Solver Server.')
    parser.add_argument('-a', metavar='address', type=str, default='localhost',
                        help='address (default: %(default)s)')
    parser.add_argument('-p', metavar='port', type=int, default=12345,
                        help='server port (default: %(default)i)')
    parser.add_argument('smtfile', metavar='smtfile', type=str,
                        help='file with a query in smt-lib2 format')
    
    args = parser.parse_args(argv)
    port = args.p
    address = args.a
    query = ''.join(open(args.smtfile).readlines())
    
    sock = gevent.socket.socket()
    sock.connect((address, port))
    
    tests.common.send_new_query(sock, query)
    
    mes = ReplyMessage()
    
    tests.common.recv_to_message(sock, mes)
    
    if mes.type == ReplyMessage.SAT:
        print 'SAT'
        print mes.sat.assignment
    elif mes.type == ReplyMessage.UNSAT:
        print 'UNSAT'
    else:
        assert 0
    print 'stats: '
    print mes.stats







if __name__ == '__main__':
    main(sys.argv[1:])