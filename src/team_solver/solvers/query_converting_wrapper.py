import copy
from team_solver.interfaces.interfaces import ISolver
from team_solver.solvers.converters import ConversionException

import gevent


class QueryConvertingWrapper(ISolver):
    def __init__(self, klee_to_smt1_converter, solver):
        self._solver = solver
        self._klee_to_smt1 = klee_to_smt1_converter
        self._greenlet = None

    def solve_async(self, uniq_query, callbackOK, callbackError):
        #TODO: 0: ah, use AsyncCanceableAction
        assert self._greenlet is None
        self._greenlet = gevent.spawn(self._solve, uniq_query, callbackOK, callbackError)

    def _solve(self, uniq_query, callbackOK, callbackError):
        self._callbackOK = callbackOK
        self._callbackError = callbackError
        self._uniq_query = uniq_query
        try:
            uniq_query_copy = copy.deepcopy(uniq_query) #prevent modifying original query
            uniq_query_copy.query = self._klee_to_smt1.convert(uniq_query.query)
            
            self._solver.solve_async(uniq_query_copy, self._callbackOKWrapper, self._callbackErrorWrapper)
        except ConversionException, e:
            callbackError(self, self._uniq_query, str(e))
        finally:
            self._greenlet = None

    #noinspection PyUnusedLocal
    def _callbackOKWrapper(self, solver, solver_result):
        assert self._uniq_query is not None
        solver_result.unique_query = self._uniq_query

        if solver_result.is_sat and solver_result.assignment:
            solver_result.assignment = self._convert_back(solver_result.assignment) #converter changes array names

        self._callbackOK(self, solver_result)

    #noinspection PyUnusedLocal
    def _callbackErrorWrapper(self, solver, uniq_query, error_desc):
        self._callbackError(self, self._uniq_query, error_desc)

    def cancel(self):
        if self._greenlet:
            self._greenlet.join()
        self._solver.cancel()

    def _convert_back(self, assignment):
        converted = {}
        for a in assignment:
            key = self._klee_to_smt1.convert_back_arr_name(a)
            converted[key] = assignment[a]
        return converted
