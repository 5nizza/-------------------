#!/usr/bin/env python

#TODO: leave the only class: BenchmarkingSolver vs SequentialBenchmarkingSolver
# the difference is in the order solvers are called:
# BenchmarkingSolver calls all solvers in parallel
# SequentialBenchmarkingSolver calls them sequentially
# When benchmarking lots of queries it is easier to paralellize the experiment with SequentialBenchmarkingSolver

import sys
import argparse
from team_solver.solvers.converters import KleeToSmt1Converter, CmdLineConverter, ConversionException
from team_solver.solvers.timed_solver_wrapper import TimedSolverWrapper

from team_solver.interfaces.interfaces import UniqueQuery, SolverException, ISolver, SolverResult

from team_solver.utils.cmd_line import add_solvers_args_to_parser, create_solvers_from_args

class SequentialBenchmarkingSolver(ISolver):
    def __init__(self, sync_solvers):
        self._solvers = sync_solvers

    def solve(self, uniq_query):
        timings = {}
        for s in self._solvers:
            try:
                solver_result = s.solve(uniq_query)
                assert len(solver_result.stats) == 1
                timings[s] = solver_result.stats.values()[0]

            except SolverException, e:
                if e.reason == 'timeout':
                    timings[s] = 'timeout'
                else:
                    timings[s] = e

        return SolverResult(uniq_query, None, timings)


def main(argv):
    parser = argparse.ArgumentParser(description='Sequential Benchmarking SMT Solver.')

    #should preceed arguments with var nargs
    parser.add_argument('klee_query_file',
                        type=str,
                        help='file with a query in klee format')
    
    parser.add_argument('-smtconverter',
                        type=str,
                        required=True,
                        help='converter command: smt2->smt1 format')

    parser.add_argument('-kleeconverter',
                        type=str,
                        required=True,
                        help='converter command: klee->smt2 format')

    parser.add_argument('-timeout',
                        metavar='timeout',
                        type=float,
                        default=120,
                        nargs= "?",
                        help='time limit(sec) for each solver (default: %(default)i)')

    add_solvers_args_to_parser(parser)

    args = parser.parse_args(argv)

    timeout = args.timeout

    with open(args.klee_query_file) as f:
        klee_query = f.read()

    #create converter
    klee_to_smt2 = CmdLineConverter(args.kleeconverter.split(' ')[0], args.kleeconverter.split(' ')[1:])
    smt2_to_smt1 = CmdLineConverter(args.smtconverter.split(' ')[0], args.smtconverter.split(' ')[1:])
    klee_to_smt1 = KleeToSmt1Converter(klee_to_smt2, smt2_to_smt1)

    #create solvers
    timed_solvers = [TimedSolverWrapper(s, timeout) for s in create_solvers_from_args(args)]
    assert len(timed_solvers) > 0, 'no solvers supplied'

    solver = SequentialBenchmarkingSolver(timed_solvers)

    #convert, solve
    try:
        smt1_query = klee_to_smt1.convert(klee_query)
        results = solver.solve(UniqueQuery(123, smt1_query))
        for s in results.stats:
            print(str(s), ": ", results.stats[s])

    except ConversionException, e:
        print("couldn't parse a query: ", e)
    except SolverException, e:
        print("solver error: ", e)


if __name__ == "__main__":
    main(sys.argv[1:])
