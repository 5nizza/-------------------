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


ev_stop = None
def sigint_handler(_=None, __=None):
    print 'received Ctr+C'
    ev_stop.set()
def work_around_infinite_wait(): # we need some active greenlet, since gevent hangs into wait/waitany functions and doesn't call signal_handler
    while True:
        if ev_stop.wait(0.5):
            break

def create_solver(solvers_args, benchmark_mode):
    solvers = [STPWrapper(args[0], args[1]) for args in solvers_args]
#    if len(solvers) == 1:
#        return solvers[0]

    if benchmark_mode:
        return BenchmarkingSolver(solvers)
    return PortfolioSolver(solvers)

#TODO: use logging module
def main(argv):
    global ev_stop
    ev_stop = gevent.event.Event()
    gevent.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGINT, sigint_handler)
    gevent.spawn(work_around_infinite_wait)
    
    #TODO: add sanity validations of input: port number, etc.
    parser = argparse.ArgumentParser(description='SMT Solver Server.')
    parser.add_argument('-p', metavar='port', type=int, default=12345,
                   help='listening port (default: %(default)i)')

    parser.add_argument('-solvers', metavar='solvers', type=str, 
                        nargs = "+",
                        default = ["/home/art_haali/projects/stp-fast-prover/trunk/stp/output/bin/stp --SMTLIB2 -p"],
                        help='solvers: cmds to run (in quotes, separated by space, e.g.: "..../stp --SMTLIB2 -p")')

    parser.add_argument('-b', 
                        dest="benchmark_mode",
                        action="store_true", 
                        default=False, 
                        help='start in a benchmarking mode (default: %(default)i)') #TODO: ah, boolean format

    args = parser.parse_args(argv)
    port = args.p

    solvers_args = []
    for sa in [x.strip('"') for x in args.solvers]:
        solver_cmd, solver_opt = sa.split()[0], sa.split()[1:]
        solvers_args.append((solver_cmd, solver_opt))

    solver = create_solver(solvers_args, args.benchmark_mode)
    cmd_channel = TcpCmdChannel("localhost", port)
    man = Manager(solver, cmd_channel)

    man.start(ev_stop) #blocking


if __name__ == '__main__':
    main(sys.argv[1:])
