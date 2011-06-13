import team_solver

__author__ = 'art_haali'


class ConversionException(Exception):
    pass

class KleeToSmt1Converter:
    def __init__(self, klee_to_smt2, smt2_to_smt1):
        self._klee_to_smt2 = klee_to_smt2
        self._smt2_to_smt1 = smt2_to_smt1

    def convert(self, klee_query):
        smt2_query = self._klee_to_smt2.convert(klee_query)
        return self._smt2_to_smt1.convert(smt2_query)

    def convert_back_arr_name(self, smt1_arr_name):
        """ conversion klee->smt1/smt2 changes array names
            Return: original klee array name
        """
        return smt1_arr_name.split('_')[0]

class CmdLineConverter:
    def __init__(self, path, opts):
        self._cmd_to_run = [path]
        self._cmd_to_run.extend(opts)

    def convert(self, klee_query):
        try:
            returned, out, err = team_solver.utils.subproc.popen_communicate(self._cmd_to_run,
                                                                             klee_query)
            if returned < 0:
                raise ConversionException("return code < 0: {0}: \nout: {1}\nerr:{2}".format(returned, out, err))

            return out
        except (OSError, IOError):
            import traceback
            raise ConversionException(traceback.format_exc())