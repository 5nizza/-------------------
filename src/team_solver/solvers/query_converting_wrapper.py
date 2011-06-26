import copy
from team_solver.interfaces.interfaces import ISolver, SolverException
from team_solver.solvers.converters import ConversionException


class QueryConvertingWrapper(ISolver):
    def __init__(self, klee_to_smt1_converter, solver):
        self._solver = solver
        self._klee_to_smt1 = klee_to_smt1_converter
        self._greenlet = None

    def solve(self, uniq_query):
        try:
            uniq_query_copy = copy.deepcopy(uniq_query) #prevent modifying original query
            uniq_query_copy.query = self._klee_to_smt1.convert(uniq_query.query)

            solver_result = self._solver.solve(uniq_query_copy)

            solver_result.unique_query = uniq_query

            if solver_result.is_sat and solver_result.assignment:
                solver_result.assignment = self._convert_back(solver_result.assignment) #converter changes array names

            return solver_result

        except ConversionException, e:
            raise SolverException(e)

    def _convert_back(self, assignment):
        converted = {}
        for a in assignment:
            key = self._klee_to_smt1.convert_back_arr_name(a)
            converted[key] = assignment[a]

        return converted