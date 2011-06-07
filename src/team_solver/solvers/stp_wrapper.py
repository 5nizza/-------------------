from team_solver.solvers.process_solver import ProcessSolver
import team_solver.utils.all

class STPWrapper(ProcessSolver):
    def __init__(self, cmd_path, cmd_options = []):
        ProcessSolver.__init__(self, cmd_path, cmd_options)
        self._name = 'STP: ({0})'.format(cmd_options)

    def parse_solver_reply(self, solver_out):
        if solver_out == None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None

        lines = [x.strip() for x in solver_out.split("\n") if x != '']
        if not lines:
            return 'unknown solver output format: {0}'.format(solver_out), None, None
        last_line = lines[-1]

        if last_line == 'unsat':
            return None, False, None
        elif last_line != 'sat':
            return "couldn't parse query status: last_line ('{1}') is not sat/unsat:\n {0}".format(solver_out, last_line), None, None

        a_lines = [_.strip() for _ in lines[:-1] if _.startswith("ASSERT")]
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000001] = 0x00 );
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000002] = 0x00 );
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000000] = 0x01 );
        #ASSERT( arr3_n_args_0x1acd8b0[0x00000003] = 0x00 );
        arrs = {}
        for l in a_lines:
            arr_name = l[l.index(' ') + 1: l.index('[')]
            index = int(l[l.index('[') + 1 : l.index(']')], 16)
            value = int(l.split('=')[1].replace(' );', '').strip(), 16)
            arrs[arr_name] = arrs.get(arr_name, {})
            arrs[arr_name][index] = value
        return None, True, team_solver.utils.all.arrs_to_assignment(arrs)

    @property
    def name(self):
        return self._name


