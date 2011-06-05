from gevent.event import Event

import utils.subproc

import sys
import traceback
import time

from team_solver.common import SolverResult

import team_solver.common as common
import gevent
from gevent.hub import GreenletExit


#TODO: 1: replace inheritance by input arg 'parser'
class ProcessSolver(common.ISolver):
    """ base class for external process based solvers """

    def __init__(self, cmd_path, cmd_options = []):
        self._cmd_args = [cmd_path]
        self._cmd_args.extend(cmd_options or [])
        self._greenlet = None #used for cancellation only

#---protected--------------------------------------------------------------
    def parse_solver_reply(self, solver_out):
        """return: parse_error, is_sat, assignment"""
        assert 0, 'abstract'

    @property
    def name(self):
        return "derived solver hasn't setup its name"

#---ISolver-----------------------------------------------------------------
    def solve_async(self, uniq_query, callbackOK, callbackError):
        assert self._greenlet == None
        self._greenlet = gevent.spawn(self._solve, uniq_query, callbackOK, callbackError)

    def cancel(self):
        if self._greenlet != None:
            self._greenlet.kill()
            self._greenlet = None #greenlet is created but not started

#---------------------------------------------------------------------------
    #TODO: ah, send is blocking => stealing time from solver
    def _solve(self, uniq_query, callbackOK, callbackError):
        try:
            start = time.time()

            returncode, out, err = utils.subproc.popen_communicate(self._cmd_args, uniq_query.query)
            if returncode < 0:
                error_desc = "return code < 0: {0}\n stdout:\n{1}\n stderr:\n{2}".format(returncode, out, err)
                callback = lambda: callbackError(self, uniq_query, error_desc)
                return

            finish = time.time()

            parse_error, is_sat, assignment = self.parse_solver_reply(out)
            if parse_error == None:
                callback = lambda: callbackOK(self, SolverResult(uniq_query, is_sat, [self._name + ": " + str(finish-start)], assignment))
            else:
                callback = lambda: callbackError(self, uniq_query, parse_error) #TODO: get rid of it?
        except GreenletExit:
            callback = lambda: True
        except Exception, e:
            print >>sys.stderr, self._name, ": FATAL error: \n", traceback.format_exc()
            callback = lambda: callbackError(self, uniq_query, e)
        finally:
            self._greenlet = None
            callback()
            
