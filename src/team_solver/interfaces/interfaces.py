"""
Created on May 13, 2011

@author: art_haali
"""

class SolverResult:
    #TODO: stats_dict -> stats, it shouldn't be a dict
    def __init__(self, unique_query, is_sat, stats_dict=None, assignment=None):
        """ assignment is dict: arr_name -> {dict index->value}
            stats is dict: solver -> StatsData
        """
        self.unique_query = unique_query
        self.is_sat = is_sat
        if is_sat:
            self.assignment = assignment
        self.stats = stats_dict if stats_dict is not None else {}


class StatsData:
    def __init__(self, time, sat_time=None, nof_sat_calls=None):
        self._time = time
        self._sat_time = sat_time
        self._nof_sat_calls = nof_sat_calls

    @property
    def time(self):
        return self._time

    @property
    def sat_time(self):
        return self._sat_time

    @property
    def nof_sat_calls(self):
        return self._nof_sat_calls

    def __str__(self):
        return 'time: {0}, sat_time: {1}, nof_sat_calls: {2}'.format(self._time, self._sat_time, self._nof_sat_calls)


class UniqueQuery:
    def __init__(self,  cmd_id, query):
        self.query = query
        self.cmd_id = cmd_id

    def __str__(self):
        return 'cmd_id: {0}: query: {1}\n'.format(self.cmd_id, self.query)


class Cmd:
    NEW_QUERY, CANCEL_QUERY = range(2)
    def __init__(self, type, query):
        self.type = type
        self.query = query


class ICmdHandler:
    def on_new_query(self, unique_query):
        raise NotImplementedError()
    def on_cancel_query(self, unique_query):
        raise NotImplementedError()


class ICmdChannel:
    def register_cmd_handler(self, cmd_handler): #can you do it better?
        raise NotImplementedError()
    def start(self):
        raise NotImplementedError()
    def stop(self):
        raise NotImplementedError()
    def send_result(self, result):
        raise NotImplementedError()

    
class SolverException(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self._reason = reason

    @property
    def reason(self):
        return self._reason


class ISolverAsync:
    def solve_async(self, unique_query, callbackOK, callbackError):
        """ Input:
            callbackOK(solver, solver_result)
            callbackError(solver, uniq_query, error_desc)
        """
        raise NotImplementedError()
    def cancel(self):
        raise NotImplementedError()


class ISolver:
    def solve(self, unique_query):
        """ Return SolverResult
            Exceptions: SolverException
        """
        raise NotImplementedError()


