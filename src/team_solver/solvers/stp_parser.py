import re
from team_solver.interfaces.interfaces import StatsData
from team_solver.solvers.process_solver import IParser
from team_solver.utils.python_ext import get_val

class STPParser(IParser):
    def parse(self, solver_out, solver_err):
        if solver_out is None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None, None

        lines = [x.strip() for x in solver_out.split("\n") if x != '']
        if not lines:
            return 'unknown solver output format: {0}'.format(solver_out), None, None, None

        last_line = lines[-1]
        if last_line == 'unsat':
            return None, False, None, None
        elif last_line != 'sat':
            return "couldn't parse query status: last_line ('{1}') is not sat/unsat:\n {0}".format(solver_out, last_line), None, None, None

        a_lines = [_.strip() for _ in lines[:-1] if _.startswith("ASSERT")]
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000001] = 0x00 );
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000002] = 0x00 );
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000000] = 0x01 );
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000003] = 0x00 );
        #sat
        arrs = {}
        for l in a_lines:
            arr_name = l[l.index(' ') + 1: l.index('[')]
            index = int(l[l.index('[') + 1 : l.index(']')], 16)
            value = int(l.split('=')[1].replace(' );', '').strip(), 16)
            arrs[arr_name] = arrs.get(arr_name, {})
            arrs[arr_name][index] = value
        return None, True, arrs, None


class STPStatsAwareParser(IParser):
    def __init__(self, stp_parser):
        self._stp_parser = stp_parser

    ### Example reply
    ### Stdout:
    #ASSERT( const_arr8_0x43ff170[0x0000017B] = 0xC0 );
    #ASSERT( arr6_n_args_0x1fd58b0[0x00000000] = 0x04 );
    #sat

    ### Stderr (## means optional output)
    #statistics
    ##Transforming: 1 [247ms]
    ##Simplifying: 8 [3309ms]
    ##Parsing: 1 [163ms]
    ##CNF Conversion: 10 [99ms]
    ##Bit Blasting: 10 [808ms]
    ##SAT Solving: 10 [740ms]
    ##Sending to SAT Solver: 10 [175ms]
    ##Counter Example Generation: 10 [132ms]
    ##Constant Bit Propagation: 3 [550ms]
    ##Array Read Refinement: 9 [26ms]
    ##Applying Substitutions: 4 [70ms]
    ##Remove Unconstrained: 2 [131ms]
    ##Pure Literals: 2 [27ms]
    ##ITE Contexts: 1 [561ms]
    ##Interval Propagation: 2 [30ms]
    #Statistics Total: 7.07s
    #CPU Time Used   : 7.29s
    #Peak Memory Used: 134.00MB
    def parse(self, out, err):
        parse_error, is_sat, assignment, _ = self._stp_parser.parse(out, err)

        if parse_error is not None:
            return parse_error, None, None, None

        err_lines = [e.strip() for e in err.split('\n')]

        nof_sat_calls, sat_time = 0, 0

        sat_re = re.compile(r'SAT Solving: (\d+) \[(\d+)ms\]')
        sat_line = get_val(err_lines, sat_re.match)
        if sat_line is not None:
            m = sat_re.match(sat_line)
            nof_sat_calls_token, sat_time_token = m.groups()
            nof_sat_calls, sat_time = int(nof_sat_calls_token), float(sat_time_token)/1000.

        time_re = re.compile(r'Statistics Total: (\d+\.?\d*)')
        time_line = get_val(err_lines, time_re.match)
        time = float(time_re.match(time_line).groups()[0])

        return None, is_sat, assignment, StatsData(time, sat_time, nof_sat_calls)


    































