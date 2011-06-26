"""""
Created on May 20, 2011

@author: art_haali
"""""
import unittest
from team_solver.solvers.async_sync_solver_wrappers import AsyncSolverWrapper
from team_solver.solvers.process_solver import ProcessSolver
from team_solver.solvers.stp_parser import STPParser
from team_solver.solvers.portfolio_solver import PortfolioSolver
from team_solver.tests import common

import team_solver.tests.common
import team_solver.interfaces.interfaces

import team_solver.utils.all

import gevent
import gevent.event

import random


class Test(unittest.TestCase):

    def _do_sat_test(self, solvers):
        ev_ok = gevent.event.Event()
        def callbackOK(s, solver_result):
            assert not ev_ok.is_set()
            assert solver_result.is_sat
            common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT_SMT)
            ev_ok.set()
        def callbackError(solver, uniq_query, err_desc): assert 0, err_desc

        solver = PortfolioSolver(solvers)
        uniq_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.SAT_QUERY_SMT)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        assert ev_ok.wait(5)

    def test_sat_query(self):
        solver1 = AsyncSolverWrapper(ProcessSolver(STPParser(), "STP", common.STP_PATH, ["--SMTLIB2", "-p"]))
        solver2 = AsyncSolverWrapper(ProcessSolver(STPParser(), "STP", common.STP_PATH, ["--SMTLIB2", "-p"]))
        self._do_sat_test([solver1, solver2])

    def test_one_solver_hanged(self):
        solver1 = AsyncSolverWrapper(ProcessSolver(STPParser(), "STP", common.STP_PATH, ["--SMTLIB2", "-p"]))
        solver2 = AsyncSolverWrapper(ProcessSolver(None, "python", "python", ["-c", "while True: pass"]))
        self._do_sat_test([solver1, solver2])

    def test_sat_stress_test(self):
        ev_ok = gevent.event.Event()
        def callbackOK(s, solver_result):
            assert not ev_ok.is_set()
            assert solver_result.is_sat
            common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT_SMT)
            ev_ok.set()
        def callbackError(solver, uniq_query, err_desc): assert 0, err_desc

        solvers = []
        for _ in range(1, 20):
            if random.random() > 1/2.:
                solver = AsyncSolverWrapper(ProcessSolver(STPParser(), "STP", common.STP_PATH, ["--SMTLIB2", "-p"]))
            else:
                solver = AsyncSolverWrapper(ProcessSolver(None, "python", "python", ["-c", "while True: pass"]))
            solvers.append(solver)

        solver = PortfolioSolver(solvers)
        for _ in range(1, 10):
            uniq_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.SAT_QUERY_SMT)
            solver.solve_async(uniq_query, callbackOK, callbackError)
            if random.random() > 1/2.:
                ev_ok.wait() #since there should be no context sw -> we can call solve_async after this wait
            else:
                solver.cancel()
            ev_ok.clear()



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()





