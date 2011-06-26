import traceback
import gevent
import sys
from gevent.hub import GreenletExit
from team_solver.interfaces.interfaces import SolverException, ISolverAsync, ISolver

class AsyncSolverWrapper(ISolverAsync):
    def __init__(self, solver_sync):
        self._solver = solver_sync
        self._greenlet = None

    def solve_async(self, uniq_query, callbackOK, callbackError):
        assert self._greenlet is None
        self._greenlet = gevent.spawn(self._solve, uniq_query, callbackOK, callbackError)

    def cancel(self):
        if self._greenlet is not None:
            self._greenlet.kill()
            self._greenlet = None #greenlet is created but not started

    def _solve(self, uniq_query, callbackOK, callbackError):
        callback = None
        try:
            solver_result = self._solver.solve(uniq_query)
            callback = lambda: callbackOK(self, solver_result)

        except SolverException, e:
            callback = lambda: callbackError(self, uniq_query, e)
        except GreenletExit:
            callback = lambda: True
        except Exception, e:
            print >>sys.stderr, str(self._solver), ": FATAL error: \n", traceback.format_exc()
            callback = lambda: callbackError(self, uniq_query, e)
        finally:
            self._greenlet = None
            callback()


class SyncSolverWrapper(ISolver):
    def __init__(self, async_solver):
        self._async_solver = async_solver

    def solve(self, uniq_query):
        self._done = gevent.event.Event()
        self._result = None
        self._error = None

        self._async_solver.solve_async(uniq_query, self._callbackOK, self._callbackError)
        self._done.wait()

        if self._error is not None:
            raise SolverException(self._error)

        assert self._result is not None
        return self._result

    @property
    def name(self):
        return self._async_solver.name

    def _callbackOK(self, solver, solver_result):
        self._result = solver_result
        self._done.set()

    def _callbackError(self, solver, uniq_query, error_desc):
        self._error = error_desc
        self._done.set()