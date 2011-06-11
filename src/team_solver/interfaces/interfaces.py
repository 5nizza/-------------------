"""
Created on May 13, 2011

@author: art_haali
"""

class SolverResult:
    def __init__(self, unique_query, is_sat, stats_dict=None, assignment=None):
        """ assignment is dict: arr_name -> {dict index->value}
            stats is dict: solver -> stats (str)
        """
        self.unique_query = unique_query
        self.is_sat = is_sat
        if is_sat:
            self.assignment = assignment
        self.stats = stats_dict if stats_dict is not None else {}


class UniqueQuery:
    def __init__(self,  cmd_id, query):
        self.query = query
        self.cmd_id = cmd_id


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

class ISolver:
    def solve_async(self, unique_query, callbackOK, callbackError):
        """ Input:
            callbackOK(solver, solver_result)
            callbackError(solver, uniq_query, error_desc)
        """
        raise NotImplementedError()
    def cancel(self):
        raise NotImplementedError()

