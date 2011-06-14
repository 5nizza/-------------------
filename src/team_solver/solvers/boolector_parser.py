import re
from team_solver.interfaces.interfaces import StatsData
from team_solver.solvers.process_solver import IParser
from team_solver.utils.python_ext import get_index, get_val

class BoolectorParser(IParser):
    def parse(self, solver_out, solver_err):
        if solver_out is None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None, None

        split = filter(lambda s: s!='', [s.strip() for s in solver_out.split('\n')])
        if len(split) < 1:
            return "couldn't get status (sat/unsat)", None, None, None
        if split[0] == 'unsat':
            return None, False, None, None
        elif split[0] != 'sat':
            return 'unknown format for status', None, None, None

#        sat
#        arr1_0x1c90aa0[0] 1
#        arr1_0x1c90aa0[1] 0
#        arr1_0x1c90aa0[2] 0
#        arr1_0x1c90aa0[3] 0
#        arr3_0x1ca21c0[1] 48
#        arr3_0x1ca21c0[0] 37
#        arr4_0x1c9c2c0[0] 1
#        arr4_0x1c9c2c0[1] 0
#        arr4_0x1c9c2c0[2] 0
#        arr4_0x1c9c2c0[3] 0

        try:
            arrs = {}
            for l in split:
                if '[' not in l:
                    continue
                l = l.strip()
                arr_name = l[0: l.index('[')]
                index = int(l[l.index('[') + 1: l.index(']')])
                value = int(l.split(' ')[1])
                a = arrs[arr_name] = arrs.get(arr_name, {}) 
                a[index] = value
        except ValueError, e:
            return 'unknown format: {0}'.format(str(e)), None, None, None

        return None, True, arrs, None


class BoolectorStatsAwareParser(IParser):
    def __init__(self, boolector_parser):
        self._boolector_parser = boolector_parser

### Stdout with options -d -pm -v -v
#[btrmain] Boolector 1.4.1 376e6b097a9a63af246339a13dd0e61b8774db77
#[btrmain] gcc (Ubuntu/Linaro 4.4.4-14ubuntu5) 4.4.5
#[btrmain] -Wall -O3 -DNDEBUG -DBTOR_USE_PRECOSAT
#[btrmain] released Fri Mar  4 19:52:48 CET 2011
#[btrmain] compiled Wed Jun  8 21:43:14 CEST 2011
#[btrmain] gcc (Ubuntu/Linaro 4.4.4-14ubuntu5) 4.4.5
#[btorsmt] initializing SMT parser
#[btorsmt] parsing SMT file /home/art_haali/data-backups/coreutils-2h-top-100-smt1/dd-lazy-merge-query3500.smt.smt1
#[btorsmt] read 188979 bytes
#[btorsmt] found 2878 symbols
#[btorsmt] generated 38210 nodes
#[btorsmt] extracting expressions
#[btorsmt] benchmark B_
#[btorsmt] found 843 constants
#[btorsat] PicoSAT Version 936
#[btrmain] parsed 7 inputs and 2 outputs
#[btrmain] logic QF_AUFBV
#[btrmain] status unknown
#[btrmain] generating SAT instance
#[btrmain] added 1 outputs (50%)
#[btrmain] added 2 outputs (100%)
#[btorexp] calling SAT
#[btorsat] refinement iteration 10
#[btorsat] refinement iteration 20
#[btorsat] refinement iteration 30
#[btorsat] refinement iteration 40
#[btorsat] refinement iteration 50
#[btorsat] refinement iteration 60
#[btorsat] refinement iteration 70
#[btorsat] refinement iteration 80
#[btorsat] refinement iteration 90
#[btorsat] refinement iteration 100
#[btorsat] refinement iteration 110
#[btorsat] refinement iteration 120
#[btorsat] refinement iteration 130
#[btorsat] refinement iteration 140
#[btorsat] refinement iteration 150
#[btorsat] refinement iteration 160
#[btorsat] refinement iteration 170
#[btorsat] refinement iteration 180
#[btorsat] refinement iteration 190
#[btorsat] refinement iteration 200
#[btorsat] refinement iteration 210
#[btorsat] refinement iteration 220
#[btorsat] refinement iteration 230
#sat
#arr6_n_args_0x1fd58b0[0] 4
#arr6_n_args_0x1fd58b0[1] 0
#arr6_n_args_0x1fd58b0[2] 0
#arr6_n_args_0x1fd58b0[3] 0
#arr4_arg3_0x2048440[1] 0
#arr4_arg3_0x2048440[0] 0
#arr2_arg1_0x2008eb0[4294967238] 0
#arr2_arg1_0x2008eb0[4294967232] 115
#arr2_arg1_0x2008eb0[4294967234] 108
#arr2_arg1_0x2008eb0[4294967233] 111
#arr2_arg1_0x2008eb0[6] 0
#arr2_arg1_0x2008eb0[5] 0
#arr2_arg1_0x2008eb0[4] 0
#arr2_arg1_0x2008eb0[3] 0
#arr2_arg1_0x2008eb0[2] 1
#arr2_arg1_0x2008eb0[1] 0
#arr2_arg1_0x2008eb0[0] 0
#arr2_arg1_0x2008eb0[4294967235] 0
#arr2_arg1_0x2008eb0[4294967236] 0
#arr2_arg1_0x2008eb0[4294967237] 0
#arr1_arg0_0x1ffeff0[6] 45
#arr1_arg0_0x1ffeff0[5] 61
#arr1_arg0_0x1ffeff0[4] 125
#arr1_arg0_0x1ffeff0[3] 128
#arr1_arg0_0x1ffeff0[2] 108
#arr1_arg0_0x1ffeff0[1] 111
#arr1_arg0_0x1ffeff0[0] 98
#arr3_arg2_0x20155d0[1] 0
#arr3_arg2_0x20155d0[0] 0
#[picosat] 1453 calls                         <------------nof_sat_calls
#[picosat] 1 iterations
#[picosat] 0 restarts
#[picosat] 35 conflicts
#[picosat] 0 adc conflicts
#[picosat] 2658522 decisions
#[picosat] 35381 fixed variables
#[picosat] 37909 learned literals
#[picosat] 13.6% deleted literals
#[picosat] 38687207 propagations
#[picosat] 59.0% variables used
#[picosat] 25.6 seconds in library           <--------------sat_time
#[picosat] 1.5 megaprops/second
#[picosat] 45 simplifications
#[picosat] 0 reductions
#[picosat] 1.1 MB recycled
#[picosat] 15.8 MB maximally allocated
#[btorexp] 0/9/8/8 constraints 0/0/0/8 22.4 MB
#[btorexp] variable substitutions: 0
#[btorexp] array substitutions: 0
#[btorexp] embedded constraint substitutions: 2
#[btorexp] assumptions: 0
#[btorexp]
#[btorexp] lemmas on demand statistics:
#[btorexp]  LOD refinements: 234
#[btorexp]  array axiom 1 conflicts: 155
#[btorexp]  array axiom 2 conflicts: 79
#[btorexp]  average lemma size: 17.3
#[btorexp]  average linking clause size: 26.2
#[btorexp]
#[btorexp] linear constraint equations: 0
#[btorexp] add normalizations: 0
#[btorexp] mul normalizations: 0
#[btorexp] read over write propagations during construction: 990
#[btorexp] synthesis assignment inconsistencies: 2
#[btorsat] resetting PicoSAT
#[btrmain] 28.5 seconds                    <----------------time
#[btrmain] 22.9 MB

    def parse(self, out, err):
        if out is None or out == '':
            return 'solver output is empty', None, None, None

        out_lines = [l.strip() for l in out.split('\n') if l.strip() != '']

        assignment_begin = get_index(out_lines, lambda s: s.startswith('sat') or s.startswith('unsat'))
        stats_begin = assignment_begin + get_index(out_lines[assignment_begin:], lambda s: s.startswith('['))
        out_wo_stats = '\n'.join(out_lines[assignment_begin:stats_begin])
        parse_error, is_sat, assignment, _ = self._boolector_parser.parse(out_wo_stats, err)

        if parse_error is not None:
            return parse_error, None, None, None

        nof_sat_calls_re = re.compile(r'\[picosat\] (\d+) calls')
        sat_time_re = re.compile(r'\[picosat\] (\d+\.?\d*) seconds in library')

        nof_sat_calls, sat_time = 0, 0

        nof_sat_calls_line = get_val(out_lines, nof_sat_calls_re.match)
        if nof_sat_calls_line is not None:
            nof_sat_calls = int(nof_sat_calls_re.match(nof_sat_calls_line).groups()[0])
            sat_time_line = get_val(out_lines, sat_time_re.match)
            sat_time = float(sat_time_re.match(sat_time_line).groups()[0])

        time = float(re.compile(r'\[btrmain\] (\d+.?\d*) seconds').match(out_lines[-2]).groups()[0])

        return None, is_sat, assignment, StatsData(time, sat_time, nof_sat_calls)
