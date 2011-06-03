from team_solver.solvers.process_solver import ProcessSolver

class BoolectorWrapper(ProcessSolver):
    def __init__(self, cmd_path, cmd_options = []):
        ProcessSolver.__init__(self, cmd_path, cmd_options)
        self._name = 'Boolector: ({0})'.format(cmd_options)

    def parse_solver_reply(self, solver_out):
        if solver_out == None or solver_out.strip() == '':
            return "parse error: solver output is empty", None, None

        assert 0, 'hmm: boolector eats smt2 format'

    @property
    def name(self):
        return self._name


