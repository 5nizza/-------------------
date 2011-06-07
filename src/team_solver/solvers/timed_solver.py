import team_solver.utils.all

import gevent
from team_solver.interfaces.interfaces import ISolver

class TimedSolver(ISolver):
    def __init__(self, solver, timeout=None):
        self._solver = solver
        self._timeout = timeout
        self._sentry = None
        self._sentry_cancelling = False

    def solve_async(self, uniq_query, callbackOK, callbackError):
        if self._timeout:
            self._sentry = gevent.spawn_later(self._timeout, self._sentry_func)
        self._callbackOK = callbackOK
        self._callbackError = callbackError
        self._uniq_query = uniq_query
        return self._solver.solve_async(uniq_query, self._callbackOKWrapper, self._callbackErrorWrapper)

    def cancel(self):
        if self._sentry and not self._sentry_cancelling:
            self._sentry.kill()
            self._sentry = None
            self._solver.cancel()

        if self._sentry_cancelling:
            self._sentry.join()
            assert not self._sentry_cancelling
            self._sentry = None


    def _callbackOKWrapper(self, solver, solver_result):
        if not self._cancel_scheduled_sentry():
            return
        self._callbackOK(solver, solver_result)

    def _callbackErrorWrapper(self, solver, uniq_query, error_desc):
        if not self._cancel_scheduled_sentry():
            return
        self._callbackError(solver, solver_result)

    def _sentry_func(self):
        #we here -> no callbacks will be called => call callbackError('timeout')
        assert self._timeout
        assert self._sentry
        self._sentry_cancelling = True
        self._solver.cancel(self._uniq_query)
        self._callbackError(self._solver, self._uniq_query, 'timeout({0})'.format(self._timeout))
        self._sentry_cancelling = False
        self._sentry = None

    def _cancel_scheduled_sentry(self):
        if self._sentry_cancelling:
            return False
        self._sentry.kill()
        self._sentry = None
        return True
