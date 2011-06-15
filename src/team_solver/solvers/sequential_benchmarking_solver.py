from team_solver.interfaces.interfaces import SolverResult, ISolver, SolverException, StatsData


#TODO: leave the only class: BenchmarkingSolver vs SequentialBenchmarkingSolver
# the difference is in the order solvers are called:
# BenchmarkingSolver calls all solvers in parallel
# SequentialBenchmarkingSolver calls them sequentially
# When benchmarking lots of queries it is easier to paralellize the experiment with SequentialBenchmarkingSolver
class SequentialBenchmarkingSolver(ISolver):
    def __init__(self, sync_solvers):
        self._solvers = sync_solvers

    def solve(self, uniq_query):
        timings = {}
        for s in self._solvers:
            try:
                solver_result = s.solve(uniq_query)
                assert len(solver_result.stats) == 1
                timings[s] = solver_result.stats.values()[0]

            except SolverException, e:
                if e.reason == 'timeout':
                    timings[s] = StatsData(float('inf'))
                else:
                    raise

        return SolverResult(uniq_query, None, timings)
