from gevent import Timeout
from team_solver.interfaces.interfaces import ISolver, SolverException

class TimedSolverWrapper(ISolver):
    def __init__(self, sync_solver, timeoutSeconds):
        assert timeoutSeconds >= 0
        self._sync_solver = sync_solver
        self._timeoutSeconds = timeoutSeconds

    def solve(self, unique_query):
        try:
            with Timeout(self._timeoutSeconds):
                return self._sync_solver.solve(unique_query)
        except Timeout:
            raise SolverException('timeout')

    def __str__(self):
        return str(self._sync_solver)
