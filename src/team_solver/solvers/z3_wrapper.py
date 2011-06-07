from team_solver.solvers.process_solver import ProcessSolver
import re
import team_solver.utils.all

class Z3Wrapper(ProcessSolver):
    def __init__(self, cmd_path, cmd_options = []):
        ProcessSolver.__init__(self, cmd_path, cmd_options)
        self._name = 'Z3: ({0})'.format(cmd_options)
        self._var_re = re.compile("(k![0-9]+)")

    def parse_solver_reply(self, solver_out):
        if solver_out == None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None

        if solver_out.split()[-1] == 'unsat':
            return None, False, None
        elif solver_out.split()[-1] != 'sat':
            return "couldn't parse status from the last line", None, None
        
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
# ------->
#arr1_0x1c90aa0 1,0,0,0
#arr3_0x1ca21c0 37,48
#arr4_0x1c9c2c0 1,0,0,0

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
                    assert cur_arr != None
                    index, value = [int(_) for _ in re.findall('bv([0-9]+)', l)]
                    cur_arr[index] = value

            return None, True, arrs
        
        except ValueError, e:
            return "unknown format: {0}".format(str(e)), None, None

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

    @property
    def name(self):
        return self._name


