import team_solver.utils.subproc

import time

from team_solver.interfaces.interfaces import SolverResult, ISolver, SolverException


class IParser:
    def parse(self, out, err):
        """ Return: parse_error, is_sat, assignment """
        raise NotImplementedError()


class ProcessSolver(ISolver):
    def __init__(self, parser, name_prefix, cmd_path, cmd_options = ()):
        self._parser = parser
        self._name = "{0}: ({1})".format(name_prefix, cmd_options)
        self._cmd_args = [cmd_path]
        self._cmd_args.extend(cmd_options)

    def solve(self, uniq_query):
        start = time.time()
        returned, out, err = team_solver.utils.subproc.popen_communicate(self._cmd_args, uniq_query.query)
        if returned < 0:
            raise SolverException("return code < 0: {0}\n stdout:\n{1}\n stderr:\n{2}".format(returned, out, err))

        finish = time.time()

        parse_error, is_sat, assignment = self._parser.parse(out, err)
        if parse_error is not None:
            raise SolverException(parse_error)

        return SolverResult(uniq_query, is_sat, {self: str(finish-start)}, assignment)

    def __str__(self):
        return self._name
