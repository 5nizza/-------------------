'''
Created on Jun 6, 2011

@author: art_haali
'''

import gevent.event
import sys
import os

import utils.subproc
from team_solver.solvers.stp_wrapper import STPWrapper
from team_solver.solvers.z3_wrapper import Z3Wrapper
from team_solver.solvers.boolector_wrapper import BoolectorWrapper
from team_solver.common import UniqueQuery

class Result:
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
        self._done.wait()
        if not self._done.is_set():
            self._solver.cancel()
            self._result = Result(False, 'timeout')
        return self._result

    def _callbackOK(self, solver, solver_result):
        self._result = Result(True, None, solver_result.stats[self._solver])
        self._done.set()

    def _callbackError(self, solver, uniq_query, error_desc):
        self._result = Result(False, error_desc)
        self._done.set()
        
class Converter:
    def __init__(self, path, opts):
        self._cmd_to_run = [path]
        self._cmd_to_run.extend(opts)

    def convert(self, klee_query):
        try:
            def logError(error):
                print >>sys.stderr, "Conversion Error: \n{0}".format(e)
            
            returncode, out, err = utils.subproc.popen_communicate(self._cmd_to_run,
                                                                   klee_query)
            if returncode < 0:
                logError("return code < 0: {0}: \nout: {1}\nerr:{2}".format(returncode, out, err))
                return None
            
            return out
        except Exception, e:
            import traceback
            logError(traceback.format_exc())
            return None

class SequentialBenchmarkingSolver:
    def __init__(self, solvers):
        self._solvers = solvers

    def solve(self, smt1_query):
        """ output: dict: solver -> time/TIMEOUT/ERROR """

        results = {}
        for s in self._solvers:
            uniq_query = UniqueQuery(123, smt1_query)
            result = s.solve(uniq_query)
            results[s] = result

        return results

def main():
    timeout = 10 #10 second
    klee_query_file = "/home/art_haali/Documents/eclipse-workspaces/python-workspace/team-solver/example-klee-query"

    klee_query = None
    with open(klee_query_file) as f:
        klee_query = "\n".join(f.readlines())

    #'-' at the end means 'read stdin'
    converter = Converter("/home/art_haali/projects/pure-klee/Release+Asserts/bin/queries-to-smt-format",
                          ['-print-to-stdout', '-output-format=smt1', '-'])

    stp_solver = STPWrapper('/home/art_haali/projects/stp-fast-prover/trunk/stp/bin/stp', 
                            ['--SMTLIB1', '-p'])
    z3_solver = Z3Wrapper("/home/art_haali/projects/smt-comparison/z3/bin/z3",
                          ['-in', '-smt', '-m'])
    boolector_wrapper = BoolectorWrapper("/home/art_haali/projects/smt-comparison/boolector-1.4.1-376e6b0-110304/boolector",
                                         ['-m', '-d', '--smt'])
    sync_solvers = [SyncSolver(s, timeout) for s in [stp_solver, z3_solver, boolector_wrapper]]
    solver = SequentialBenchmarkingSolver(sync_solvers)

    smt1_query = converter.convert(klee_query)
    print smt1_query
    if smt1_query != None:
        results = solver.solve(smt1_query)
        for r in results:
            print results[r].ok, ", time: ", results[r].time, ", error: ", results[r].error

if __name__ == "__main__":
    main()
