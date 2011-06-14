#!/usr/bin/env python

import sys
import argparse
from team_solver.solvers.boolector_parser import BoolectorStatsAwareParser, BoolectorParser
from team_solver.solvers.converters import KleeToSmt1Converter, CmdLineConverter, ConversionException
from team_solver.solvers.sequential_benchmarking_solver import SequentialBenchmarkingSolver
from team_solver.solvers.stp_parser import STPParser, STPStatsAwareParser
from team_solver.solvers.timed_solver_wrapper import TimedSolverWrapper

from team_solver.interfaces.interfaces import UniqueQuery, SolverException
from team_solver.solvers.z3_parser import Z3StatsAwareParser, Z3Parser

from team_solver.utils.cmd_line import add_solvers_args_to_parser, create_solvers

def main(argv):
    parser = argparse.ArgumentParser(description='Sequential Benchmarking SMT Solver.')

    #should precede arguments with var nargs
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
    z3_solvers = create_solvers(lambda: Z3StatsAwareParser(Z3Parser()), 'Z3', args.z3_solvers)
    stp_solvers = create_solvers(lambda: STPStatsAwareParser(STPParser()), 'STP', args.stp_solvers)
    boolector_solvers = create_solvers(lambda: BoolectorStatsAwareParser(BoolectorParser()), 'Boolector',
                                       args.boolector_solvers)
    timed_solvers = [TimedSolverWrapper(s, timeout) for s in z3_solvers+stp_solvers+boolector_solvers]
    assert len(timed_solvers) > 0, 'no solvers supplied'

    solver = SequentialBenchmarkingSolver(timed_solvers)

    #convert, solve
    try:
        smt1_query = klee_to_smt1.convert(klee_query)
        results = solver.solve(UniqueQuery(123, smt1_query))
        for s in results.stats:
            print str(s), ": ", str(results.stats[s])

    except ConversionException, e:
        print("couldn't parse a query: ", e)
    except SolverException, e:
        print("solver error: ", e)


if __name__ == "__main__":
    main(sys.argv[1:])
