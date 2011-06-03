'''
Created on May 26, 2011

@author: art_haali
'''

import team_solver.common
import sys

class PortfolioSolver(team_solver.common.ISolver):
    def __init__(self, solvers):
        self._solvers = solvers

#---ISolver-----------------------------------------------------------------
    def solve_async(self, uniq_query, callbackOK, callbackError):
        self._solved = 0
        self._errored = 0
        self._callbackOK = callbackOK
        self._callbackError = callbackError

        for s in self._solvers:
            s.solve_async(uniq_query, self._on_solved, self._on_error)

    def cancel(self):
        self.cancel_others()
        
#----------------------------------------------------------------------------        
    def _on_solved(self, solver, solver_result):
        if self._solved > 0: #since s.cancel() causes context switching -> many greenlets can enter here
            return 
        self._solved += 1
        self.cancel_others(solver)
        self._callbackOK(solver, solver_result)

    def _on_error(self, solver, uniq_query, err_desc):
        if self._errored > 0: #since s.cancel() causes context switching -> many greenlets can enter here
            return
        self._errored += 1
        self.cancel_others(solver)
        self._callbackError(solver, uniq_query, err_desc)#----------------------------------------------------------------------------

#----------------------------------------------------------------------------      
    def cancel_others(self, solver_to_leave=None):
        for s in self._solvers:
            if s != solver_to_leave:
                s.cancel()
