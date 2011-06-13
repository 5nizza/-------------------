from team_solver.solvers.portfolio_solver import PortfolioSolver

class BenchmarkingSolver(PortfolioSolver):
    def __init__(self, solvers):
        PortfolioSolver.__init__(self, solvers)
        self._init_state()

    def _init_state(self):
        self._stats = {}
        self._solved = 0
        self._errored = 0
        self._solver_result = None

#----------------------------------------------------------------------------
    def _on_solved(self, solver, solver_result):
        self._solver_result = solver_result
        self._solved += 1
        self._stats.update(solver_result.stats)
        if self._solved + self._errored == len(self._PortfolioSolver__solvers):
            solver_result.stats = self._stats
            self._PortfolioSolver__callbackOK(self, solver_result)
            self._init_state()

    def _on_error(self, solver, uniq_query, err_desc): #also on timeout
        self._errored += 1
        self._stats.update({solver: err_desc})
        if self._errored + self._solved == len(self._PortfolioSolver__solvers):
            if self._solved > 0:
                solver_result = self._solver_result
                solver_result.stats = self._stats
                self._PortfolioSolver__callbackOK(self, solver_result)
            else:
                assert len(self._stats) == len(self._PortfolioSolver__solvers)
                self._PortfolioSolver__callbackError(self, uniq_query, self._errors_to_str(self._stats))
            self._init_state()

    def _errors_to_str(self, stats):
        result = ''
        for s in stats:
            if result != '':
                result += '\n'
            result += stats[s]
        return result



