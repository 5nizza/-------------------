from team_solver.interfaces.interfaces import StatsData
from team_solver.solvers.process_solver import IParser
import re

class Z3Parser(IParser):
    def __init__(self):
        self._var_re = re.compile("(k![0-9]+)")

    def parse(self, solver_out, solver_err):
        if solver_out is None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None, None

        if solver_out.split()[-1] == 'unsat':
            return None, False, None, None
        elif solver_out.split()[-1] != 'sat':
            return "couldn't parse status from the last line: out:\n{0}".format(solver_out), None, None, None

#(define arr4_0x1c9c2c0 as-array[k!0])
#(define arr3_0x1ca21c0 as-array[k!1])
#(define arr1_0x1c90aa0 as-array[k!2])
#(define (k!0 (x1 (bv 32)))
#  (if (= x1 bv0[32]) bv1[8]
#  (if (= x1 bv2[32]) bv0[8]
#  (if (= x1 bv1[32]) bv0[8]
#  (if (= x1 bv3[32]) bv0[8]
#    bv0[8])))))
#(define (k!1 (x1 (bv 32)))
#  (if (= x1 bv0[32]) bv37[8]
#  (if (= x1 bv1[32]) bv48[8]
#    bv37[8])))
#(define (k!2 (x1 (bv 32)))
#  (if (= x1 bv3[32]) bv0[8]
#  (if (= x1 bv2[32]) bv0[8]
#  (if (= x1 bv1[32]) bv0[8]
#  (if (= x1 bv0[32]) bv1[8]
#    bv0[8])))))
#sat

        try:
            arrname_by_var = self._get_arr_var(solver_out)
            arrs = {}
            cur_arr = None
            for l in solver_out.split('\n'):
                l = l.strip()
                if l.startswith('(define ('):
                    var_name = self._var_re.search(l).groups()[0]
                    arrs[arrname_by_var[var_name]] = cur_arr = {}
                if l.startswith('(if'):
                    assert cur_arr is not None
                    index, value = [int(_) for _ in re.findall('bv([0-9]+)', l)]
                    cur_arr[index] = value

            return None, True, arrs, None
        
        except ValueError, e:
            return "unknown format: {0}".format(str(e)), None, None, None

    def _get_arr_var(self, solver_out):
        arr_by_var = {}
        for l in solver_out.split('\n'):
            l = l.strip()
            if l.startswith('(define'):
                if 'as-array' in l: #(define arr4_0x1c9c2c0 as-array[k!0])
                    arr_name = l.split()[1]
                    var_name = self._var_re.search(l).groups()[0]
                    arr_by_var[var_name] = arr_name

        return arr_by_var


class Z3StatsAwareParser(IParser):
    def __init__(self, z3_parser):
        self._z3_parser = z3_parser
        
    def parse(self, solver_out, solver_err):
        try:
            lines = [l.strip() for l in solver_out.split('\n') if l.strip() != '']

            stats_start = None
            for i, l in enumerate(lines):
                if l.startswith('num.'):
                    stats_start = i
                    break

            if stats_start is None:
                return 'stats not found', None, None, None

            #time:               0 secs
            timing = float(lines[-1].split()[1])
        except ValueError, e:
            return e, None, None, None

        solver_out_without_stats = '\n'.join(lines[0:stats_start])
        error, is_sat, assignment, _ = self._z3_parser.parse(solver_out_without_stats, solver_err)

        return error, is_sat, assignment, StatsData(timing)
