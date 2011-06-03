from team_solver.solvers.process_solver import ProcessSolver

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

        is_sat = None
        if last_line == 'sat':
            is_sat = True
        elif last_line == 'unsat':
            is_sat = False
        else:
            return "couldn't parse query status: last_line ('{1}') is not sat/unsat:\n {0}".format(solver_out, last_line), None, None

        if not is_sat:
            return None, False, None
        
        assignment = [l for l in lines[:-1] if l.startswith("ASSERT")]

        return None, True, '\n'.join(assignment)
    
    @property
    def name(self):
        return self._name


