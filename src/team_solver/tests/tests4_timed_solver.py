'''
Created on May 20, 2011

@author: art_haali
'''
import unittest

import common
import team_solver.interfaces.interfaces

import team_solver.utils.all

import gevent
import gevent.event
from team_solver.solvers.timed_solver import TimedSolver
from team_solver.interfaces.interfaces import ISolver, UniqueQuery
from team_solver.tests.common import MockSolver


class Test(unittest.TestCase):
    def test_timeout(self):
        ev_error = gevent.event.Event()
        def callbackOK(_, solver_result): assert 0
        def callbackError(_, uniq_query, err_desc): 
            assert 'timeout' in err_desc
            ev_error.set()

        solver = TimedSolver(MockSolver(), 0.001)
        uniq_query = UniqueQuery(123, common.SAT_QUERY)
        solver.solve_async(uniq_query, callbackOK, callbackError)

        assert ev_error.wait(5)
        solver.cancel()
        #no exceptions

    def test_cancel(self):
        ev_error = gevent.event.Event()
        def callbackOK(_, solver_result): assert 0
        def callbackError(_, uniq_query, err_desc): assert 0

        solver = TimedSolver(MockSolver(), 99)
        uniq_query = UniqueQuery(123, common.SAT_QUERY)
        solver.solve_async(uniq_query, callbackOK, callbackError)
        gevent.sleep(1) #wait until greenlet spawned
        solver.cancel()

        solver.solve_async(uniq_query, callbackOK, callbackError)
        solver.cancel() #immediately
        #no exceptions

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


