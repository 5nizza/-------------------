import unittest


import gevent
import gevent.event
from team_solver.solvers.timed_solver import TimedSolver
from team_solver.interfaces.interfaces import UniqueQuery, SolverResult
from team_solver.tests import common
from team_solver.tests.common import MockSolver


class Test(unittest.TestCase):
    def test_without_timeout(self):
        ev_ok = gevent.event.Event()
        def callbackOK(_, solver_result): ev_ok.set()
        def callbackError(_, uniq_query, err_desc): assert 0

        mock_solver = MockSolver()
        solver = TimedSolver(mock_solver)
        uniq_query = UniqueQuery(123, common.SAT_QUERY_SMT)
        solver.solve_async(uniq_query, callbackOK, callbackError)
        mock_solver.raise_solved(SolverResult(uniq_query, False))
        assert ev_ok.wait(5)
        #no exceptions

    def test_timeout(self):
        ev_error = gevent.event.Event()
        def callbackOK(_, solver_result): assert 0
        def callbackError(_, uniq_query, err_desc): 
            assert 'timeout' in err_desc
            ev_error.set()

        solver = TimedSolver(MockSolver(), 0.001)
        uniq_query = UniqueQuery(123, common.SAT_QUERY_SMT)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        assert ev_error.wait(5)
        solver.cancel()
        #no exceptions

    def test_cancel(self):
        ev_error = gevent.event.Event()
        def callbackOK(_, solver_result): assert 0
        def callbackError(_, uniq_query, err_desc): assert 0

        solver = TimedSolver(MockSolver(), 99)
        uniq_query = UniqueQuery(123, common.SAT_QUERY_SMT)
        solver.solve_async(uniq_query, callbackOK, callbackError)
        gevent.sleep(1) #wait until greenlet spawned
        solver.cancel()

        solver.solve_async(uniq_query, callbackOK, callbackError)
        solver.cancel() #immediately
        #no exceptions

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


