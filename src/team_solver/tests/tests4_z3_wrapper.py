'''
Created on May 20, 2011

@author: art_haali
'''
import unittest
from team_solver.solvers.stp_wrapper import STPWrapper

import common
import team_solver.common

import utils.all

import gevent
import gevent.event
from team_solver.solvers.z3_wrapper import Z3Wrapper

arr1 = ('arr4_0x1c9c2c0', [1, 0, 0, 0])
arr2 = ('arr3_0x1ca21c0', [37, 48])
arr3 = ('arr1_0x1c90aa0', [1, 0, 0, 0])
example_reply = """(define arr4_0x1c9c2c0 as-array[k!0])
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

class Test(unittest.TestCase):
    def test_parsing_sat(self):
        solver = Z3Wrapper('', '')
        parse_error, is_sat, assignment = solver.parse_solver_reply(example_reply)
        assert parse_error == None
        assert is_sat
        a_expected = {arr1[0]:arr1[1], arr2[0]:arr2[1], arr3[0]:arr3[1]}
        common.assert_sat_assignments(a_expected, assignment)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


