#!/usr/bin/env python

import argparse
import sys
import signal

import gevent
import gevent.event

from team_solver.manager.manager import Manager

from team_solver.cmd_channels.tcp_cmd_channel import TcpCmdChannel
from team_solver.solvers.async_sync_solver_wrappers import AsyncSolverWrapper
from team_solver.solvers.async_sync_solver_wrappers import SyncSolverWrapper
from team_solver.solvers.converters import KleeToSmt1Converter, CmdLineConverter

from team_solver.solvers.portfolio_solver import PortfolioSolver
from team_solver.solvers.benchmarking_solver import BenchmarkingSolver
from team_solver.solvers.query_converting_wrapper import QueryConvertingWrapper
from team_solver.solvers.timed_solver_wrapper import TimedSolverWrapper
from team_solver.utils.cmd_line import add_solvers_args_to_parser, create_solvers_from_args


ev_stop = None
#noinspection PyUnusedLocal
def sigint_handler(_=None, __=None):
    print 'received Ctr+C'
    ev_stop.set()
def work_around_infinite_wait(): # we need some active greenlet, since gevent hangs into wait/wait_any functions and doesn't call signal_handler
    while True:
        if ev_stop.wait(0.5):
            break

#TODO: use logging module
def main(argv):
    global ev_stop
    ev_stop = gevent.event.Event()
    gevent.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGINT, sigint_handler)
    gevent.spawn(work_around_infinite_wait)

    #TODO: add sanity validations of input: port number, etc.
    parser = argparse.ArgumentParser(description='SMT Solver Server.')
    parser.add_argument('-p', dest = 'port', type=int, default=12345,
                        help='listening port (default: %(default)i)')

    parser.add_argument('-timeout', dest = 'timeout', type=int, default=360,
                        help='solving timeout(sec.) for a query (benchmarking mode only) (default: %(default)i)')

    parser.add_argument('-smtconverter',
                        type=str,
                        required=True,
                        help='converter command: smt2->smt1 format')

    parser.add_argument('-kleeconverter',
                        type=str,
                        required=True,
                        help='converter command: klee->smt2 format')

    add_solvers_args_to_parser(parser)

    args = parser.parse_args(argv)

    port = args.port

    sync_solvers = create_solvers_from_args(args)
    print "Created {0} solvers to feed PortfolioSolver".format(len(sync_solvers))
    if not sync_solvers:
        print 'Provide input solvers.'
        return

    sync_solver = PortfolioSolver([AsyncSolverWrapper(s) for s in sync_solvers])

    klee_to_smt2 = CmdLineConverter(args.kleeconverter.split(' ')[0], args.kleeconverter.split(' ')[1:])
    smt2_to_smt1 = CmdLineConverter(args.smtconverter.split(' ')[0], args.smtconverter.split(' ')[1:])
    klee_to_smt1 = KleeToSmt1Converter(klee_to_smt2, smt2_to_smt1)

    solver = AsyncSolverWrapper(QueryConvertingWrapper(klee_to_smt1, SyncSolverWrapper(sync_solver)))

    cmd_channel = TcpCmdChannel("localhost", port)
    man = Manager(solver, cmd_channel)

    man.start(ev_stop) #blocking

if __name__ == '__main__':
    main(sys.argv[1:])
