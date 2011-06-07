#!/usr/bin/env python
'''
Created on May 12, 2011

@author: art_haali
'''

import argparse
import sys
import signal

import gevent.event

from team_solver.manager.manager import Manager

from team_solver.cmd_channels.tcp_cmd_channel import TcpCmdChannel

from team_solver.solvers.stp_wrapper import STPWrapper
from team_solver.solvers.portfolio_solver import PortfolioSolver
from team_solver.solvers.benchmarking_solver import BenchmarkingSolver
from team_solver.solvers.boolector_wrapper import BoolectorWrapper
from team_solver.solvers.z3_wrapper import Z3Wrapper
from team_solver.solvers.timed_solver import TimedSolver
from team_solver.utils.cmd_line import add_solvers_args_to_parser,\
    create_solvers_from_args


ev_stop = None
def sigint_handler(_=None, __=None):
    print 'received Ctr+C'
    ev_stop.set()
def work_around_infinite_wait(): # we need some active greenlet, since gevent hangs into wait/waitany functions and doesn't call signal_handler
    while True:
        if ev_stop.wait(0.5):
            break

#TODO: 1: use logging module
def main(argv):
    global ev_stop
    ev_stop = gevent.event.Event()
    gevent.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGINT, sigint_handler)
    gevent.spawn(work_around_infinite_wait)

    #TODO: 1: add sanity validations of input: port number, etc.
    parser = argparse.ArgumentParser(description='SMT Solver Server.')
    parser.add_argument('-p', metavar='port', dest = 'port', type=int, default=12345,
                        help='listening port (default: %(default)i)')

    parser.add_argument('-b', 
                        dest="benchmark_mode",
                        action="store_true", 
                        default=False, 
                        help='start in a benchmarking mode (default: %(default)r)')
    
    parser.add_argument('-timeout', metavar='timeout', dest = 'timeout', type=int, default=360,
                        help='solving timeout(sec.) for a query (benchmarking mode only) (default: %(default)i)')

    add_solvers_args_to_parser(parser)

    args = parser.parse_args(argv)

    port = args.port

    all_solvers = create_solvers_from_args(args)
    print "Created {0} solvers to feed {1}".format(len(all_solvers),
                                                   ['PortfolioSolver', 'BenchmarkingSolver'][args.benchmark_mode])
    if not all_solvers:
        print 'Provide input solvers.'
        return

    solver = None
    if args.benchmark_mode:
        solvers = [TimedSolver(s) for s in all_solvers]
        solver = BenchmarkingSolver(all_solvers)
    else:
        solver = PortfolioSolver(all_solvers)

    cmd_channel = TcpCmdChannel("localhost", port)
    man = Manager(solver, cmd_channel)

    man.start(ev_stop) #blocking

if __name__ == '__main__':
    main(sys.argv[1:])
