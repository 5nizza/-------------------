'''
Created on May 20, 2011

@author: art_haali
'''
import unittest
from team_solver.solvers.stp_wrapper import STPWrapper
from team_solver.solvers.portfolio_solver import PortfolioSolver

import common
import team_solver.common

import utils.all

import gevent
import gevent.event

import random


class Test(unittest.TestCase):

    def do_sat_test(self, solvers):
        ev_ok = gevent.event.Event()
        def callbackOK(s, solver_result):
            assert not ev_ok.is_set()
            assert solver_result.is_sat
            common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT)
            ev_ok.set()
        def callbackError(uniq_query, err_desc): assert 0

        solver = PortfolioSolver(solvers)
        uniq_query = team_solver.common.UniqueQuery(123, common.SAT_QUERY)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        assert ev_ok.wait(5)

    def test_sat_query(self):
        solver1 = STPWrapper(common.STP_PATH, ["--SMTLIB2", "-p"])
        solver2 = STPWrapper(common.STP_PATH, ["--SMTLIB2", "-p"])
        self.do_sat_test([solver1, solver2])

    def test_one_solver_hanged(self):
        solver1 = STPWrapper(common.STP_PATH, ["--SMTLIB2", "-p"])
        solver2 = STPWrapper("python", ["-c", "while True: pass"])
        self.do_sat_test([solver1, solver2])

    def test_sat_stress_test(self):
        ev_ok = gevent.event.Event()
        def callbackOK(s, solver_result):
            assert not ev_ok.is_set()
            assert solver_result.is_sat
            common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT)
            ev_ok.set()
        def callbackError(uniq_query, err_desc): assert 0

        solvers = []
        for _ in range(1, 20):
            if random.random() > 1/2.:
                solver = STPWrapper(common.STP_PATH, ["--SMTLIB2", "-p"])
            else:
                solver = STPWrapper("python", ["-c", "while True: pass"])
            solvers.append(solver)

        solver = PortfolioSolver(solvers)
        for _ in range(1, 10):
            uniq_query = team_solver.common.UniqueQuery(123, common.SAT_QUERY)
            solver.solve_async(uniq_query, callbackOK, callbackError)
            if random.random() > 1/2.:
                ev_ok.wait() #since there should be no context sw -> we can call solve_async after this wait
            else:
                solver.cancel()
            ev_ok.clear()



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()





