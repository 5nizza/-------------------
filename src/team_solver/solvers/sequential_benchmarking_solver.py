from team_solver.interfaces.interfaces import SolverResult, ISolver, SolverException, StatsData

class SequentialBenchmarkingSolver(ISolver):
    def __init__(self, sync_solvers):
        self._solvers = sync_solvers

    def solve(self, uniq_query):
        stats = {}
        for s in self._solvers:
            try:
                solver_result = s.solve(uniq_query)
                assert len(solver_result.stats) == 1
                stats[s] = solver_result.stats.values()[0]

            except SolverException, e:
                if e.reason == 'timeout':
                    stats[s] = StatsData(float('inf'))
                else:
                    raise

        return SolverResult(uniq_query, None, stats)
