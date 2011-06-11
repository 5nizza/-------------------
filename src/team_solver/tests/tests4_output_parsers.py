import unittest
from team_solver.solvers.z3_wrapper import Z3Wrapper
from team_solver.solvers.boolector_wrapper import BoolectorWrapper
from team_solver.tests import common

z3_example_reply = """(define arr4_0x1c9c2c0 as-array[k!0])
(define arr3_0x1ca21c0 as-array[k!1])
(define arr1_0x1c90aa0 as-array[k!2])
(define (k!0 (x1 (bv 32)))
  (if (= x1 bv0[32]) bv1[8]
  (if (= x1 bv2[32]) bv0[8]
  (if (= x1 bv1[32]) bv0[8]
  (if (= x1 bv3[32]) bv0[8]
    bv0[8])))))
(define (k!1 (x1 (bv 32)))
  (if (= x1 bv0[32]) bv37[8]
  (if (= x1 bv1[32]) bv48[8]
    bv37[8])))
(define (k!2 (x1 (bv 32)))
  (if (= x1 bv3[32]) bv0[8]
  (if (= x1 bv2[32]) bv0[8]
  (if (= x1 bv1[32]) bv0[8]
  (if (= x1 bv0[32]) bv1[8]
    bv0[8])))))
sat"""

boolector_example_reply = """
sat
arr1_0x1c90aa0[0] 1
arr1_0x1c90aa0[1] 0
arr1_0x1c90aa0[2] 0
arr1_0x1c90aa0[3] 0
arr3_0x1ca21c0[1] 48
arr3_0x1ca21c0[0] 37
arr4_0x1c9c2c0[0] 1
arr4_0x1c9c2c0[1] 0
arr4_0x1c9c2c0[2] 0
arr4_0x1c9c2c0[3] 0
"""

assignment_expected = {'arr4_0x1c9c2c0':{0:1, 1:0, 2:0, 3:0}, 
                       'arr3_0x1ca21c0':{0:37, 1:48},
                       'arr1_0x1c90aa0': {0:1, 1:0, 2:0, 3:0}}

class Test(unittest.TestCase):
    
    def _do_test(self, parser, reply_to_parse):
        parse_error, is_sat, assignment = parser.parse_solver_reply(reply_to_parse, None)
        assert parse_error is None, parse_error
        assert is_sat
        common.assert_sat_assignments(assignment_expected, assignment)

    def test_z3_parsing_sat(self):
        self._do_test(Z3Wrapper('', ''), z3_example_reply)

    def test_boolector_parsing_sat(self):
        self._do_test(BoolectorWrapper('', ''), boolector_example_reply)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


