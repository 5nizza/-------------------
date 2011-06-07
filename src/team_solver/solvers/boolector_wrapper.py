from team_solver.solvers.process_solver import ProcessSolver

import team_solver.utils.all

class BoolectorWrapper(ProcessSolver):
    def __init__(self, cmd_path, cmd_options = []):
        #TODO: 1: ah, check that this options are set (for parsing): -m -d
        ProcessSolver.__init__(self, cmd_path, cmd_options)
        self._name = 'Boolector: ({0})'.format(cmd_options)

    def parse_solver_reply(self, solver_out):
        if solver_out == None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None

        splitted = filter(lambda s: s!='', [s.strip() for s in solver_out.split('\n')])
        if len(splitted) < 1:
            return "couldn't get status (sat/unsat)", None, None
        if splitted[0] == 'unsat':
            return None, False, None
        elif splitted[0] != 'sat':
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
            for l in splitted:
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

    @property
    def name(self):
        return self._name


