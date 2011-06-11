"""
Created on May 13, 2011

@author: art_haali
"""
from sys import stderr

import team_solver.utils.all

from team_solver.interfaces.interfaces import ICmdHandler

import gevent.event

class Manager(ICmdHandler):
    LOG_PREFIX = 'Manager: '
    def __init__(self, solver, cmd_channel):
        self._solver = solver
        self._cmd_channel = cmd_channel
        self._cmd_channel.register_cmd_handler(self)
        self._queries = []
        self._solver_is_busy = False
        self._ev_next_query = gevent.event.Event()


    def start(self, ev_stop):
        self._cmd_channel.start()
        print self.LOG_PREFIX, 'started'
        while True:
            ev = team_solver.utils.all.wait_any([ev_stop, self._ev_next_query])
            if ev == self._ev_next_query:
                self._ev_next_query.clear()
                self._schedule_next_query()
                continue
            if ev == ev_stop:
                self._cmd_channel.stop()
                break

        print self.LOG_PREFIX, 'stopped'

#---ICmdHandler----------------------------------------------------------------
    def on_new_query(self, uniq_query):
        self._queries.append(uniq_query)
        self._ev_next_query.set()

    def on_cancel_query(self, uniq_query):
        if uniq_query in self._queries:
            self._queries.remove(uniq_query)
        else:
            if not self._solver_is_busy:  #client doesn't know yet that the query has already been processed
                return

            self._solver.cancel() #context switching call
            self._solver_is_busy = False
            self._ev_next_query.set()

#---SolverHandler--------------------------------------------------------------

    #noinspection PyUnusedLocal
    def _on_solver_ok(self, solver, solver_result):
        self._cmd_channel.send_result(solver_result) #context switching call(?)
        self._solver_is_busy = False #TODO: ah, get rid of
        self._ev_next_query.set()

    def _on_solver_error(self, solver, uniq_query, error):
        #TODO: 0: ah: send error
        print >>stderr, 'error in solver: {0}\n{1}\n query{2}'.format(solver.name, error, uniq_query)
        self._solver_is_busy = False
        self._ev_next_query.set()

    def _schedule_next_query(self):
        #TODO: 1: validate input data before send to solver
        if self._solver_is_busy == False and self._queries:
            uniq_query = self._queries.pop(0)
            self._solver_is_busy = True
            self._solver.solve_async(uniq_query, self._on_solver_ok, self._on_solver_error)







