import unittest

from team_solver.solvers.benchmarking_solver import BenchmarkingSolver

import common
import team_solver.interfaces.interfaces

import team_solver.utils.all

import gevent
import gevent.event

import random
from team_solver.tests.common import MockSolver
from team_solver.interfaces.interfaces import SolverResult, UniqueQuery
from team_solver.solvers.stp_wrapper import STPWrapper



class Test(unittest.TestCase):
    def test_sat_query(self):
        ev_ok = gevent.event.Event()
        def callbackOK(s, solver_result):
            assert not ev_ok.is_set()
            assert solver_result.is_sat
            assert len(solver_result.stats) == 2
            common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT)
            ev_ok.set()
        def callbackError(uniq_query, err_desc): assert 0

        solver1 = MockSolver()
        solver2 = MockSolver()
        solver = BenchmarkingSolver([solver1, solver2])

        uniq_query = UniqueQuery(123, common.SAT_QUERY)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        solver1.raise_solved(SolverResult(uniq_query, True, {solver1: '123'}, common.SAT_QUERY_ASSIGNMENT))
        solver2.raise_solved(SolverResult(uniq_query, True, {solver2: '222'}, common.SAT_QUERY_ASSIGNMENT))

        assert ev_ok.wait(5)

    def test_all_timeout_error(self):
        ev_error = gevent.event.Event()
        def callbackOK(_, solver_result): assert 0
        def callbackError(_, uniq_query, err_desc):
            assert not ev_error.is_set()
            ev_error.set()

        solver1 = MockSolver()
        solver2 = MockSolver()
        solver = BenchmarkingSolver([solver1, solver2])

        uniq_query = UniqueQuery(123, common.SAT_QUERY)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        solver1.raise_error(uniq_query, 'error!')
        solver2.raise_error(uniq_query, 'error!')

        assert ev_error.wait(5)

    def test_solved_and_timeout(self):
        ev_ok = gevent.event.Event()
        def callbackOK(_, solver_result):
            assert not ev_ok.is_set()
            ev_ok.set()
        def callbackError(_, uniq_query, err_desc): assert 0

        solver1 = MockSolver()
        solver2 = MockSolver()
        solver = BenchmarkingSolver([solver1, solver2])

        uniq_query = UniqueQuery(123, common.SAT_QUERY)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        solver1.raise_error(uniq_query, 'error!')
        solver2.raise_solved(SolverResult(uniq_query, True, {solver2: '222'}, common.SAT_QUERY_ASSIGNMENT))

        assert ev_ok.wait(5)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()





