'''
Created on May 26, 2011

@author: art_haali
'''

import team_solver.common
import sys
from team_solver.solvers.portfolio_solver import PortfolioSolver

#TODO: 2: ah, minor: add tests
class BenchmarkingSolver(PortfolioSolver):
    def __init__(self, solvers):
        PortfolioSolver.__init__(self, solvers)
        self._init_state()

    def _init_state(self):
        self._stats = {}
        self._solved = 0
        self._errored = 0

#----------------------------------------------------------------------------
    def _on_solved(self, solver, solver_result):
        self._solved += 1
        self._stats.update(solver_result.stats)
        if self._solved == len(self._PortfolioSolver__solvers):
            solver_result.stats = self._stats
            self._PortfolioSolver__callbackOK(solver, solver_result)
            self._init_state()

    def _on_error(self, solver, uniq_query, err_desc):
        if self._errored > 0: #since s.cancel() causes context switching -> many greenlets can enter here
            return
        self._errored += 1
        self._PortfolioSolver__cancel_others(solver)
        self._PortfolioSolver__callbackError(solver, uniq_query, err_desc)
        self._init_state()


