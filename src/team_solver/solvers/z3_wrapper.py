from team_solver.solvers.process_solver import ProcessSolver

class Z3Wrapper(ProcessSolver):
    def __init__(self, cmd_path, cmd_options = []):
        ProcessSolver.__init__(self, cmd_path, cmd_options)
        self._name = 'Z3: ({0})'.format(cmd_options)

    def parse_solver_reply(self, solver_out):
        if solver_out == None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None

        is_sat = False
        if solver_out.split()[-1] == 'sat':
            is_sat = True
        elif solver_out.split()[-1] == 'unsat':
            is_sat = False
        else:
            return "couldn't parse status from the last line", None, None
        
        #TODO: ah, parse assignment
        return None, is_sat, None

    @property
    def name(self):
        return self._name


