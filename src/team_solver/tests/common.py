'''
Created on May 24, 2011

@author: art_haali
'''
from team_solver.interfaces.interfaces import ISolver

STP_PATH = "/home/art_haali/projects/stp-fast-prover/trunk/stp/output/bin/stp"
Z3_PATH = "/home/art_haali/projects/smt-comparison/z3/bin/z3"


SAT_QUERY = r"""
(set-logic QF_ABV)
(set-info :smt-lib-version 2.0)
(set-info :status unknown)
(declare-fun arr3_n_args_0x1acd8b0 () (Array (_ BitVec 32) (_ BitVec 8) ))
(assert (let ((?let_k_0 (concat (select arr3_n_args_0x1acd8b0 (_ bv3 32)) (concat (select arr3_n_args_0x1acd8b0 (_ bv2 32)) (concat (select arr3_n_args_0x1acd8b0 (_ bv1 32)) (select arr3_n_args_0x1acd8b0 (_ bv0 32))))) ))
(and (and (not (bvslt (_ bv1 32) ?let_k_0)) (not (= (_ bv0 64) (bvxor (_ bv1 64) (ite (bvslt (_ bv2 32) ?let_k_0) (_ bv1 64) (_ bv0 64)))))) (bvslt (_ bv0 32) ?let_k_0)) )  
)
(check-sat)
(exit)
"""
SAT_QUERY_ASSIGNMENT = {'arr3_n_args_0x1acd8b0':{0:1, 1:0, 2:0, 3:0}}
SAT_QUERY_ASSIGNMENT_SERIALIZED = ['arr3_n_args_0x1acd8b0[0]=1',
                                   'arr3_n_args_0x1acd8b0[1]=0',
                                   'arr3_n_args_0x1acd8b0[2]=0',
                                   'arr3_n_args_0x1acd8b0[3]=0']

UNSAT_QUERY = r"""
(set-logic QF_ABV)
(set-info :smt-lib-version 2.0)
(set-info :status unknown)
(declare-fun arr3_n_args_0x1acd8b0 () (Array (_ BitVec 32) (_ BitVec 8) ))
(assert (let ((?let_k_0 (bvxor (_ bv4294967295 32) (concat (select arr3_n_args_0x1acd8b0 (_ bv3 32)) (concat (select arr3_n_args_0x1acd8b0 (_ bv2 32)) (concat (select arr3_n_args_0x1acd8b0 (_ bv1 32)) (select arr3_n_args_0x1acd8b0 (_ bv0 32)))))) )) 
(let ((?let_k_1 (concat (select arr3_n_args_0x1acd8b0 (_ bv3 32)) (concat (select arr3_n_args_0x1acd8b0 (_ bv2 32)) (concat (select arr3_n_args_0x1acd8b0 (_ bv1 32)) (select arr3_n_args_0x1acd8b0 (_ bv0 32)))))))
(and (and (and (not (bvult ?let_k_0 (_ bv4294966272 32))) (= (_ bv3 64) (concat ((_ extract 60 0) ((_ sign_extend 32) (bvsub (_ bv0 32) ?let_k_0))) (_ bv0 3)))) (not (= (_ bv0 64) (bvxor (_ bv1 64) (ite (bvslt (_ bv2 32) ?let_k_1) (_ bv1 64) (_ bv0 64)))))) (bvslt (_ bv1 32) ?let_k_1))) )  
)
(check-sat)
(exit)
"""

from team_solver.cmd_channels.team_solver_messages_pb2  import CommandMessage
from team_solver.cmd_channels.team_solver_messages_pb2 import ReplyMessage

import struct
import team_solver.utils.all

last_id = 0

def send_new_query(sock, query=SAT_QUERY):
    global last_id
    mes = CommandMessage()
    mes.type = CommandMessage.NEW_QUERY
    mes.cmdId = last_id
    last_id += 1
    mes.newQuery.query = query
    new_query_mes_as_string = mes.SerializeToString()
    sock.sendall(struct.pack('I', len(new_query_mes_as_string)))
    sock.sendall(new_query_mes_as_string)
    return mes.cmdId

def send_cancel_query(sock, cmd_id):
    cancel_query_mes = CommandMessage()
    cancel_query_mes.type = CommandMessage.CANCEL_QUERY
    cancel_query_mes.cmdId = cmd_id
    cancel_query_mes_as_string = cancel_query_mes.SerializeToString()
    sock.sendall(struct.pack('I', len(cancel_query_mes_as_string)))
    sock.sendall(cancel_query_mes_as_string)

#TODO: extract common functions, use them in cmd_channel
def recv_to_message(sock, mes, ev_cancel=None):
    mes_size = struct.unpack("I", team_solver.utils.all.recv_size(sock, 4))[0]
    message_as_string = team_solver.utils.all.recv_size(sock, mes_size, ev_cancel)
    mes.ParseFromString(message_as_string)

def assert_sat_assignments(a1, a2):
    """ input: {arr_name -> { index->value} } """
    assert len(a1) == len(a2), '{0} vs {1}'.format(len(a1), len(a2))
    for arr_name in a1:
        assert arr_name in a2
        assert a1[arr_name] == a2[arr_name], '{0} vs {1}'.format(a1[arr_name], a2[arr_name])

def assert_sat_ser_assignments(ser_a1, ser_a2):
    """ input: serialized assignments """
    a1 = ser_a1
    a2 = ser_a2
    assert len(a1) == len(a2), '{0} vs {1}'.format(len(a1), len(a2))
    for a in a1:
        assert a in a2

def emptyCallbackOK(solver, solver_result):
    pass

def emptyCallbackError(solver, uniq_query, error_desc):
    pass

class MockSolver(ISolver):
    
    def solve_async(self, unique_query, callbackOK = emptyCallbackOK, callbackError = emptyCallbackError):
        self._callbackOK = callbackOK
        self._callbackError = callbackError

    def cancel(self, uniq_query):
        pass

    def raise_solved(self, solver_result):
        self._callbackOK(self, solver_result)
        
    def raise_error(self, uniq_query, error_desc):
        self._callbackError(self, uniq_query, error_desc)
