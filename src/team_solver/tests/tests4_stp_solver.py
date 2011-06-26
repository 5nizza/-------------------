import unittest
from team_solver.solvers.process_solver import ProcessSolver
from team_solver.solvers.stp_parser import STPParser
from team_solver.tests import common

import team_solver.tests.common
import team_solver.interfaces.interfaces

import team_solver.utils.all

#REFACTOR: move to tests4_output_parsers, and test parsing only
class Test(unittest.TestCase):
    def test_sat_query(self):
        solver = ProcessSolver(STPParser(), "STP", common.STP_PATH, ["--SMTLIB2", "-p"])
        uniq_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.SAT_QUERY_SMT)
        solver_result = solver.solve(uniq_query)
        assert solver_result.is_sat
        common.assert_sat_assignments(solver_result.assignment, common.SAT_QUERY_ASSIGNMENT_SMT)

    def test_unsat_query(self):
        solver = ProcessSolver(STPParser(), "STP", common.STP_PATH, ["--SMTLIB2", "-p"])
        uniq_query = team_solver.interfaces.interfaces.UniqueQuery(123, common.UNSAT_QUERY_SMT)
        solver_result = solver.solve(uniq_query)
        assert solver_result is not None
        assert not solver_result.is_sat


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


