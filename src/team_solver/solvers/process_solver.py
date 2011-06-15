import team_solver.utils.subproc
from team_solver.interfaces.interfaces import SolverResult, ISolver, SolverException


class IParser:
    def parse(self, out, err):
        """ Return: parse_error, is_sat, assignment, stats_data (of StatsData type) """
        raise NotImplementedError()


class ProcessSolver(ISolver):
    def __init__(self, parser, name, cmd_path, cmd_options = ()):
        self._parser = parser
        self._name = name
        self._cmd_args = [cmd_path]
        self._cmd_args.extend(cmd_options)

    def solve(self, uniq_query):
        returned, out, err = team_solver.utils.subproc.popen_communicate(self._cmd_args, uniq_query.query)
        if returned < 0:
            raise SolverException("return code < 0: {0}\n stdout:\n{1}\n stderr:\n{2}".format(returned, out, err))

        parse_error, is_sat, assignment, stats_data = self._parser.parse(out, err)
        if parse_error is not None:
            raise SolverException(parse_error)

        return SolverResult(uniq_query, is_sat, {self: stats_data}, assignment)

    @property
    def name(self):
        return self._name

    @property
    def config_args(self):
        return self._cmd_args[1:]

    def __str__(self):
        return "{0}: ({1})".format(self.name, self.config_args)
