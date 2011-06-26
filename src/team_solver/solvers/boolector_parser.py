from team_solver.solvers.process_solver import IParser

class BoolectorParser(IParser):
    def parse(self, solver_out, solver_err):
        if solver_out is None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None

        split = filter(lambda s: s!='', [s.strip() for s in solver_out.split('\n')])
        if len(split) < 1:
            return "couldn't get status (sat/unsat)", None, None
        if split[0] == 'unsat':
            return None, False, None
        elif split[0] != 'sat':
            return 'unknown format for status', None, None

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
            return 'unknown format: {0}'.format(str(e)), None, None

        return None, True, arrs
