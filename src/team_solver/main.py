#!/usr/bin/env python
'''
Created on May 12, 2011

@author: art_haali
'''

from team_solver.cmd_channels.tcp_cmd_channel import TcpCmdChannel

import team_solver.manager

import signal
import gevent.event
from team_solver.solvers.stp_wrapper import STPWrapper
from team_solver.manager import Manager

import argparse
import sys
from team_solver.solvers.portfolio_solver import PortfolioSolver
from team_solver.solvers.benchmarking_solver import BenchmarkingSolver
from team_solver.solvers.boolector_wrapper import BoolectorWrapper
from team_solver.solvers.z3_wrapper import Z3Wrapper


ev_stop = None
def sigint_handler(_=None, __=None):
    print 'received Ctr+C'
    ev_stop.set()
def work_around_infinite_wait(): # we need some active greenlet, since gevent hangs into wait/waitany functions and doesn't call signal_handler
    while True:
        if ev_stop.wait(0.5):
            break

def create_solvers(ctor, solvers_args):
    cmds_opts = [(sa.split()[0], sa.split()[1:]) for sa in solvers_args]
    return [ctor(a[0], a[1]) for a in cmds_opts]

#TODO: 1: use logging module
def main(argv):
    global ev_stop
    ev_stop = gevent.event.Event()
    gevent.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGINT, sigint_handler)
    gevent.spawn(work_around_infinite_wait)
    
    #TODO: 1: add sanity validations of input: port number, etc.
    parser = argparse.ArgumentParser(description='SMT Solver Server.')
    parser.add_argument('-p', metavar='port', type=int, default=12345,
                   help='listening port (default: %(default)i)')
    
    parser.add_argument('-b', 
                        dest="benchmark_mode",
                        action="store_true", 
                        default=False, 
                        help='start in a benchmarking mode (default: %(default)i)') #TODO: 2: ah, boolean format

    parser.add_argument('-stp', metavar='stp-solver', type=str, 
                        dest = "stp_solvers",
                        nargs = "*",
                        default=[],
#                        default = ["/home/art_haali/projects/stp-fast-prover/trunk/stp/output/bin/stp --SMTLIB2 -p"],
                        help='add stp solvers (cmds in quotes, separated by space, e.g.: "..../stp --SMTLIB2 -p")')

    parser.add_argument('-z3', metavar='z3-solver', type=str,
                        dest = "z3_solvers",
                        nargs = "*",
                        default=[],
                        help='add z3 solvers (cmd in quotes, separated by space, e.g.: "..../z3 -in -smt2 -m")')

    parser.add_argument('-boolector', metavar='boolector-solver', type=str,
                        dest = "boolector_solvers",
                        nargs = "*",
                        default=[],
                        help='add boolector solvers (cmd in quotes, separated by space, e.g.: "..../boolector -m -d")')

    args = parser.parse_args(argv)
    port = args.p

    stp_solvers = create_solvers(STPWrapper, args.stp_solvers)
    z3_solvers = create_solvers(Z3Wrapper, args.z3_solvers)
    boolector_solvers = create_solvers(BoolectorWrapper, args.boolector_solvers)

    all_solvers = stp_solvers + z3_solvers + boolector_solvers

    solver = None
    print "Created {0} solvers".format(len(all_solvers))
    if args.benchmark_mode:
        solver = BenchmarkingSolver(all_solvers)
    else:
        solver = PortfolioSolver(all_solvers)

    cmd_channel = TcpCmdChannel("localhost", port)
    man = Manager(solver, cmd_channel)

    man.start(ev_stop) #blocking


if __name__ == '__main__':
    main(sys.argv[1:])
