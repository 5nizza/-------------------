"""""
Created on May 20, 2011

@author: art_haali
"""""
import unittest
from team_solver.solvers.stp_wrapper import STPWrapper
from team_solver.tests import common

import team_solver.tests.common
import team_solver.interfaces.interfaces

import team_solver.utils.all

import gevent
import gevent.event

#TODO: 2: ah, rename and test processor only
class Test(unittest.TestCase):
    #TODO: help for 'strange thing: if main thread dies => this func return empty out'
    def test_cancel_hanged_solver(self):
        def callbackOK(_, solver_result): assert 0
        def callbackError(_, any_query, err_desc): assert 0, err_desc
        solver = STPWrapper("python", ['-c', 'while True: pass'])
        any_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.SAT_QUERY_SMT)
        solver.solve_async(any_query, callbackOK, callbackError)
        solver.cancel()
        #if it starts => OK
        solver.solve_async(any_query, callbackOK, callbackError)
        solver.cancel()

    def test_sat_query(self):
        ev_ok = gevent.event.Event()
        def callbackOK(_, solver_result):
            assert solver_result.is_sat
            common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT_SMT)
            ev_ok.set()
        def callbackError(_, uniq_query, err_desc): assert 0

        solver = STPWrapper(common.STP_PATH, ["--SMTLIB2", "-p"])
        uniq_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.SAT_QUERY_SMT)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        assert ev_ok.wait(5)

    def test_unsat_query(self):
        ev_ok = gevent.event.Event()
        self.solver_result = None
        def callbackOK(solver, solver_result):
            self.solver_result = solver_result
            ev_ok.set()
        def callbackError(_, uniq_query, err_desc): assert 0

        solver = STPWrapper(common.STP_PATH, ["--SMTLIB2", "-p"])
        uniq_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.UNSAT_QUERY_SMT)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        assert ev_ok.wait(5)
        assert self.solver_result is not None
        assert not self.solver_result.is_sat


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


