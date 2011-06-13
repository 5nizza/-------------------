"""""
Created on May 26, 2011

@author: art_haali
"""""

from team_solver.interfaces.interfaces import ISolver

class PortfolioSolver(ISolver):
    def __init__(self, solvers):
        self.__solvers = solvers

#---ISolver-----------------------------------------------------------------
    def solve_async(self, uniq_query, callbackOK, callbackError):
        self._solved = 0
        self._errored = 0
        self.__callbackOK = callbackOK
        self.__callbackError = callbackError

        for s in self.__solvers:
            s.solve_async(uniq_query, self._on_solved, self._on_error)

    def cancel(self):
        self.__cancel_others()

#----------------------------------------------------------------------------        
    def _on_solved(self, solver, solver_result):
        if self._solved > 0: #since s.cancel() causes context switching -> many greenlets can enter here
            return
        self._solved += 1
        self.__cancel_others(solver)
        self.__callbackOK(self, solver_result)

    def _on_error(self, solver, uniq_query, err_desc):
        if self._errored > 0: #since s.cancel() causes context switching -> many greenlets can enter here
            return
        self._errored += 1
        self.__cancel_others(solver)
        self.__callbackError(self, uniq_query, err_desc)

#----------------------------------------------------------------------------      
    def __cancel_others(self, solver_to_leave=None):
        for s in self.__solvers:
            if s is not solver_to_leave:
                s.cancel()
