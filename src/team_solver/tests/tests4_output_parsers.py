import unittest
from team_solver.solvers.stp_parser import STPStatsAwareParser, STPParser
from team_solver.solvers.z3_parser import Z3Parser
from team_solver.solvers.boolector_parser import BoolectorParser, BoolectorStatsAwareParser
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
                       'arr1_0x1c90aa0':{0:1, 1:0, 2:0, 3:0}}

class Test(unittest.TestCase):

    def _do_test(self, parser, reply_to_parse):
        parse_error, is_sat, assignment, stats_data = parser.parse(reply_to_parse, None)
        assert parse_error is None, parse_error
        assert is_sat
        assert stats_data is None
        common.assert_sat_assignments(assignment_expected, assignment)

    def test_z3_parsing_sat(self):
        self._do_test(Z3Parser(), z3_example_reply)

    def test_boolector_parsing_sat(self):
        self._do_test(BoolectorParser(), boolector_example_reply)

    def test_boolector_stats_aware_parser(self):
        stdout = """
[btrmain] Boolector 1.4.1 376e6b097a9a63af246339a13dd0e61b8774db77
[btrmain] gcc (Ubuntu/Linaro 4.4.4-14ubuntu5) 4.4.5
[btrmain] -Wall -O3 -DNDEBUG -DBTOR_USE_PRECOSAT
[btrmain] released Fri Mar  4 19:52:48 CET 2011
[btrmain] compiled Wed Jun  8 21:43:14 CEST 2011
[btrmain] gcc (Ubuntu/Linaro 4.4.4-14ubuntu5) 4.4.5
[btorsmt] initializing SMT parser
[btorsmt] parsing SMT file /home/art_haali/data-backups/coreutils-2h-top-100-smt1/dd-lazy-merge-query3500.smt.smt1
[btorsmt] read 188979 bytes
[btorsmt] found 2878 symbols
[btorsmt] generated 38210 nodes
[btorsmt] extracting expressions
[btorsmt] benchmark B_
[btorsmt] found 843 constants
[btorsat] PicoSAT Version 936
[btrmain] parsed 7 inputs and 2 outputs
[btrmain] logic QF_AUFBV
[btrmain] status unknown
[btrmain] generating SAT instance
[btrmain] added 1 outputs (50%)
[btrmain] added 2 outputs (100%)
[btorexp] calling SAT
[btorsat] refinement iteration 10
[btorsat] refinement iteration 20
[btorsat] refinement iteration 30
[btorsat] refinement iteration 40
[btorsat] refinement iteration 50
[btorsat] refinement iteration 60
[btorsat] refinement iteration 70
[btorsat] refinement iteration 80
[btorsat] refinement iteration 90
[btorsat] refinement iteration 100
[btorsat] refinement iteration 110
[btorsat] refinement iteration 120
[btorsat] refinement iteration 130
[btorsat] refinement iteration 140
[btorsat] refinement iteration 150
[btorsat] refinement iteration 160
[btorsat] refinement iteration 170
[btorsat] refinement iteration 180
[btorsat] refinement iteration 190
[btorsat] refinement iteration 200
[btorsat] refinement iteration 210
[btorsat] refinement iteration 220
[btorsat] refinement iteration 230
sat
arr3_arg2_0x20155d0[1] 0
[picosat] 1453 calls                         <------------nof_sat_calls
[picosat] 1 iterations
[picosat] 0 restarts
[picosat] 35 conflicts
[picosat] 0 adc conflicts
[picosat] 2658522 decisions
[picosat] 35381 fixed variables
[picosat] 37909 learned literals
[picosat] 13.6% deleted literals
[picosat] 38687207 propagations
[picosat] 59.0% variables used
[picosat] 25.6 seconds in library           <--------------sat_time
[picosat] 1.5 megaprops/second
[picosat] 45 simplifications
[picosat] 0 reductions
[picosat] 1.1 MB recycled
[picosat] 15.8 MB maximally allocated
[btorexp] 0/9/8/8 constraints 0/0/0/8 22.4 MB
[btorexp] variable substitutions: 0
[btorexp] array substitutions: 0
[btorexp] embedded constraint substitutions: 2
[btorexp] assumptions: 0
[btorexp]
[btorexp] lemmas on demand statistics:
[btorexp]  LOD refinements: 234
[btorexp]  array axiom 1 conflicts: 155
[btorexp]  array axiom 2 conflicts: 79
[btorexp]  average lemma size: 17.3
[btorexp]  average linking clause size: 26.2
[btorexp]
[btorexp] linear constraint equations: 0
[btorexp] add normalizations: 0
[btorexp] mul normalizations: 0
[btorexp] read over write propagations during construction: 990
[btorexp] synthesis assignment inconsistencies: 2
[btorsat] resetting PicoSAT
[btrmain] 28.5 seconds                    <----------------time
[btrmain] 22.9 MB
        """

        assignment_expected = {'arr3_arg2_0x20155d0': {1:0}}

        parse_error, is_sat, assignment, stats_data = BoolectorStatsAwareParser(BoolectorParser()).parse(stdout, '')

        assert parse_error is None, parse_error
        assert is_sat == True, is_sat
        common.assert_sat_assignments(assignment_expected, assignment)
        assert stats_data.nof_sat_calls == 1453, stats_data
        assert stats_data.sat_time == 25.6, stats_data
        assert stats_data.time == 28.5, stats_data


    def test_stp_stats_aware_parser(self):
        stdout ="""
        ASSERT( const_arr8_0x43ff170[0x0000017B] = 0xC0 );
        ASSERT( arr6_n_args_0x1fd58b0[0x00000000] = 0x04 );
        sat"""

        stderr = """
        statistics
        Transforming: 1 [247ms]
        Simplifying: 8 [3309ms]
        Parsing: 1 [163ms]
        CNF Conversion: 10 [99ms]
        Bit Blasting: 10 [808ms]
        SAT Solving: 10 [740ms]
        Sending to SAT Solver: 10 [175ms]
        Counter Example Generation: 10 [132ms]
        Constant Bit Propagation: 3 [550ms]
        Array Read Refinement: 9 [26ms]
        Applying Substitutions: 4 [70ms]
        Remove Unconstrained: 2 [131ms]
        Pure Literals: 2 [27ms]
        ITE Contexts: 1 [561ms]
        Interval Propagation: 2 [30ms]
        Statistics Total: 7.07s
        CPU Time Used   : 7.29s
        Peak Memory Used: 134.00MB"""

        assignment_expected = {'const_arr8_0x43ff170':{379:192},
                               'arr6_n_args_0x1fd58b0': {0:4}}

        parse_error, is_sat, assignment, stats_data = STPStatsAwareParser(STPParser()).parse(stdout, stderr)

        assert parse_error is None, parse_error
        assert is_sat == True, is_sat
        common.assert_sat_assignments(assignment_expected, assignment)
        assert stats_data.nof_sat_calls == 10, stats_data
        assert stats_data.sat_time == 0.74, stats_data
        assert stats_data.time == 7.07, stats_data


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


