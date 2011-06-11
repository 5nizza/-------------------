#!/usr/bin/env python

import gevent.event
import sys
import argparse

import team_solver.utils.subproc
from team_solver.interfaces.interfaces import UniqueQuery

from team_solver.utils.cmd_line import add_solvers_args_to_parser, create_solvers_from_args

class SolverResult:
    def __init__(self, is_ok, error_desc, time=None):
        self.ok = is_ok
        self.error = error_desc
        self.time = time

class SyncSolver:
    def __init__(self, solver, timeout):
        self._timeout = timeout
        self._solver = solver

    def solve(self, uniq_query):
        self._done = gevent.event.Event()
        self._result = None
        self._solver.solve_async(uniq_query, self._callbackOK, self._callbackError)
        if not self._done.wait(self._timeout):
            self._solver.cancel()
            self._result = SolverResult(False, 'timeout')
        return self._result

    @property
    def name(self):
        return self._solver.name

    def _callbackOK(self, solver, solver_result):
        self._result = SolverResult(True, None, solver_result.stats[solver])
        self._done.set()

    def _callbackError(self, solver, uniq_query, error_desc):
        self._result = SolverResult(False, 'error in solver {0}: \n{1} \n query: {2}'.format(solver.name, error_desc, uniq_query))
        self._done.set()

class KleeToSmtQueryConverter:
    def __init__(self, path, opts):
        self._cmd_to_run = [path]
        self._cmd_to_run.extend(opts)

    def convert(self, klee_query):
        try:
            def logError(error):
                print >>sys.stderr, "Conversion Error: \n{0}".format(error)

            returncode, out, err = team_solver.utils.subproc.popen_communicate(self._cmd_to_run,
                                                                   klee_query)
            if returncode < 0:
                logError("return code < 0: {0}: \nout: {1}\nerr:{2}".format(returncode, out, err))
                return None

            return out
        except:
            import traceback
            logError(traceback.format_exc())
            return None

class SequentialBenchmarkingSolver:
    def __init__(self, sync_solvers):
        self._solvers = sync_solvers

    def solve(self, smt1_query):
        """ Return: dict: solver -> SolverResult """
        results = {}
        for s in self._solvers:
            uniq_query = UniqueQuery(123, smt1_query)
            result = s.solve(uniq_query)
            results[s] = result

        return results

def main(argv):
    parser = argparse.ArgumentParser(description='Sequential Benchmarking SMT Solver.')

    #should preceed arguments with var nargs
    parser.add_argument('klee_query_file',
                        type=str,
                        help='file with a query in klee format')
    
    parser.add_argument('-converter', metavar="'path to converter'", type=str, 
                        dest = "converter_cmd",
                        required=True,
                        help='klee->smt converter tool that reads from cin and outputs to cout(e.g. \'.../queries-to-smt-format -print-to-stdout -output-format=smt1 -\'')

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

    assert klee_query is not None and klee_query != ''
    assert args.converter_cmd is not None and args.converter_cmd != ''

    #create converter
    converter = KleeToSmtQueryConverter(args.converter_cmd.split()[0], args.converter_cmd.split()[1:])

    #create solvers
    sync_solvers = [SyncSolver(s, timeout) for s in create_solvers_from_args(args)]
    assert len(sync_solvers) > 0, 'no solvers supplied'
    solver = SequentialBenchmarkingSolver(sync_solvers)

    #convert, solve
    smt1_query = converter.convert(klee_query)
    if smt1_query is not None:
        results = solver.solve(smt1_query)
        for r in results:
            print r.name, ": ", results[r].ok, ", time: ", results[r].time, ", error: ", results[r].error


if __name__ == "__main__":
    main(sys.argv[1:])
