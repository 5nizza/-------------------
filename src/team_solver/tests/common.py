"""""
Created on May 24, 2011

@author: art_haali
"""""
from team_solver.interfaces.interfaces import ISolver

STP_PATH = "/home/art_haali/projects/stp-fast-prover/trunk/stp/output/bin/stp"
Z3_PATH = "/home/art_haali/projects/smt-comparison/z3/bin/z3"
KLEE_CONVERTER = "/home/art_haali/Documents/eclipse-workspaces/python-workspace/team-solver/queries-to-smt-format -output-format=smt2 -print-to-stdout -optimize-divides=1 -"
SMT_CONVERTER = "/home/art_haali//projects/smt-comparison/cvc3-nightly-build-2011-04-01/cvc3-2011-04-01-i686-linux-opt -lang smt2 +translate -output-lang smtlib"

SAT_QUERY_KLEE = r"""
# Query 30 -- Type: InitialValues, Instructions: 9250
array const_arr1[24] : w32 -> w8 = [224 234 158 2 0 0 0 0 112 254 91 2 0 0 0 0 171 171 171 171 171 171 171 171]
array arr1[4] : w32 -> w8 = symbolic
array arr3[4] : w32 -> w8 = symbolic
(query [(Ult N0:(ReadLSB w32 0 arr1)
             4)
        (Slt 0 N0)
        (Eq false (Slt 1 N0))
        (Eq false
            (Eq 45
                N1:(Read w8 (Extract w32 0 (Add w64 18446744073669968272
                                                    (ReadLSB w64 8 U0:[(Add w32 7
                                                                                N2:(Extract w32 0 (Mul w64 8
                                                                                                           (SExt w64 (Sub w32 0

                (Select w32 (Ult 4294966272 N3:(Xor w32 4294967295 N0))

                            N3

                            4294966272))))))=0,
                                                                       (Add w32 6 N2)=0,
                                                                       (Add w32 5 N2)=0,
                                                                       (Add w32 4 N2)=0,
                                                                       (Add w32 3 N2)=0,
                                                                       (Add w32 2 N2)=0,
                                                                       (Add w32 1 N2)=0,
                                                                       N2=0] @ const_arr1)))
                            [3=0] @ arr3)))]
       (Eq 0 N1) []
       [arr1
        arr3])
#   OK -- Elapsed: 0.002226
#   Solvable: true
#     arr1 = [1,0,0,0]
#     arr3 = [1,0,0,0]
"""


SAT_QUERY_SMT = r"""
(set-logic QF_ABV)
(set-info :smt-lib-version 2.0)
(set-info :status unknown)
(declare-fun const_arr1_0xff50c0 () (Array (_ BitVec 32) (_ BitVec 8) ))
(declare-fun arr1_0xfe8870 () (Array (_ BitVec 32) (_ BitVec 8) ))
(declare-fun arr3_0xff6c40 () (Array (_ BitVec 32) (_ BitVec 8) ))
(assert (let ((?let_k_0 (concat (select arr1_0xfe8870 (_ bv3 32)) (concat (select arr1_0xfe8870 (_ bv2 32)) (concat (select arr1_0xfe8870 (_ bv1 32)) (select arr1_0xfe8870 (_ bv0 32))))) ))
(let ((?let_k_1 (bvxor (_ bv4294967295 32) ?let_k_0)))
(let ((?let_k_2 ((_ extract 31 0) (concat ((_ extract 60 0) ((_ sign_extend 32) (bvsub (_ bv0 32) (ite (bvult (_ bv4294966272 32) ?let_k_1) ?let_k_1 (_ bv4294966272 32))))) (_ bv0 3)))))
(let ((?let_k_3 (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store const_arr1_0xff50c0 (_ bv0 32) (_ bv224 8)) (_ bv1 32) (_ bv234 8)) (_ bv2 32) (_ bv158 8)) (_ bv3 32) (_ bv2 8)) (_ bv4 32) (_ bv0 8)) (_ bv5 32) (_ bv0 8)) (_ bv6 32) (_ bv0 8)) (_ bv7 32) (_ bv0 8)) (_ bv8 32) (_ bv112 8)) (_ bv9 32) (_ bv254 8)) (_ bv10 32) (_ bv91 8)) (_ bv11 32) (_ bv2 8)) (_ bv12 32) (_ bv0 8)) (_ bv13 32) (_ bv0 8)) (_ bv14 32) (_ bv0 8)) (_ bv15 32) (_ bv0 8)) (_ bv16 32) (_ bv171 8)) (_ bv17 32) (_ bv171 8)) (_ bv18 32) (_ bv171 8)) (_ bv19 32) (_ bv171 8)) (_ bv20 32) (_ bv171 8)) (_ bv21 32) (_ bv171 8)) (_ bv22 32) (_ bv171 8)) (_ bv23 32) (_ bv171 8)) ?let_k_2 (_ bv0 8)) (bvadd (_ bv1 32) ?let_k_2) (_ bv0 8)) (bvadd (_ bv2 32) ?let_k_2) (_ bv0 8)) (bvadd (_ bv3 32) ?let_k_2) (_ bv0 8)) (bvadd (_ bv4 32) ?let_k_2) (_ bv0 8)) (bvadd (_ bv5 32) ?let_k_2) (_ bv0 8)) (bvadd (_ bv6 32) ?let_k_2) (_ bv0 8)) (bvadd (_ bv7 32) ?let_k_2) (_ bv0 8))))
(let ((?let_k_4 (select (store arr3_0xff6c40 (_ bv3 32) (_ bv0 8)) ((_ extract 31 0) (bvadd (_ bv18446744073669968272 64) (concat (select ?let_k_3 (_ bv15 32)) (concat (select ?let_k_3 (_ bv14 32)) (concat (select ?let_k_3 (_ bv13 32)) (concat (select ?let_k_3 (_ bv12 32)) (concat (select ?let_k_3 (_ bv11 32)) (concat (select ?let_k_3 (_ bv10 32)) (concat (select ?let_k_3 (_ bv9 32)) (select ?let_k_3 (_ bv8 32))))))))))))))
(and (and (and (and (and true (bvult ?let_k_0 (_ bv4 32))) (bvslt (_ bv0 32) ?let_k_0)) (not (bvslt (_ bv1 32) ?let_k_0))) (not (= (_ bv45 8) ?let_k_4))) (not (= (_ bv0 8) ?let_k_4))))))) )
)
(check-sat)
(exit)
"""

SAT_QUERY_ASSIGNMENT_KLEE = {'arr1':{0:1, 1:0, 2:0, 3:0},
                        'arr3':{0:1, 1:0, 2:0, 3:0}}
SAT_QUERY_ASSIGNMENT_SERIALIZED_KLEE = ['arr1[0]=1',
                                   'arr1[1]=0',
                                   'arr1[2]=0',
                                   'arr1[3]=0',
#STP doesn't print values that are irrelevant
                                   'arr3[0]=1']

SAT_QUERY_ASSIGNMENT_SMT = {'arr1_0xfe8870':{0:1, 1:0, 2:0, 3:0},
                            'arr3_0xff6c40':{0:1}}
SAT_QUERY_ASSIGNMENT_SERIALIZED_SMT = ['arr1_0xfe8870[0]=1',
                                   'arr1_0xfe8870[1]=0',
                                   'arr1_0xfe8870[2]=0',
                                   'arr1_0xfe8870[3]=0',
#STP doesn't print values that are irrelevant
                                   'arr3_0xff6c40[0]=1']

UNSAT_QUERY_KLEE = r"""
# Query 4 -- Type: InitialValues, Instructions: 6508
array arr1[4] : w32 -> w8 = symbolic
(query [(Ult N0:(ReadLSB w32 0 arr1)
             4)
        (Slt 0 N0)
        (Eq false (Slt 1 N0))]
       (Eq 24
           (Shl w64 (SExt w64 (Sub w32 1
                                       (Select w32 (Ult 4294966272 N1:(Xor w32 4294967295 N0))
                                                   N1
                                                   4294966272)))
                    3)) []
       [arr1])
#   OK -- Elapsed: 0.00109297
#   Solvable: false
"""

UNSAT_QUERY_SMT = r"""
(set-logic QF_ABV)
(set-info :smt-lib-version 2.0)
(set-info :status unknown)
(declare-fun arr1_0xfe8870 () (Array (_ BitVec 32) (_ BitVec 8) ))
(assert (let ((?let_k_0 (concat (select arr1_0xfe8870 (_ bv3 32)) (concat (select arr1_0xfe8870 (_ bv2 32)) (concat (select arr1_0xfe8870 (_ bv1 32)) (select arr1_0xfe8870 (_ bv0 32))))) ))
(let ((?let_k_1 (bvxor (_ bv4294967295 32) ?let_k_0)))
(and (and (and (and true (bvult ?let_k_0 (_ bv4 32))) (bvslt (_ bv0 32) ?let_k_0)) (not (bvslt (_ bv1 32) ?let_k_0))) (not (= (_ bv24 64) (concat ((_ extract 60 0) ((_ sign_extend 32) (bvsub (_ bv1 32) (ite (bvult (_ bv4294966272 32) ?let_k_1) ?let_k_1 (_ bv4294966272 32))))) (_ bv0 3)))))) )
)
(check-sat)
(exit)
"""

from team_solver.cmd_channels.team_solver_messages_pb2  import CommandMessage

import struct
import team_solver.utils.all

last_id = 0

#noinspection PyUnresolvedReferences
def send_new_query(sock, query):
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

#noinspection PyUnresolvedReferences
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
        assert arr_name in a2, "arr_name '{0}' is not in a2".format(arr_name, a2)
        assert a1[arr_name] == a2[arr_name], '{2}: {0} vs {1}'.format(a1[arr_name], a2[arr_name], arr_name)

def assert_sat_ser_assignments(ser_a1, ser_a2):
    """ input: serialized assignments """
    a1 = ser_a1
    a2 = ser_a2
    assert len(a1) == len(a2), '{0} vs {1}: \n{2}\n{3}'.format(len(a1), len(a2), a1, a2)
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

    def cancel(self):
        pass

    def raise_solved(self, solver_result):
        self._callbackOK(self, solver_result)
        
    def raise_error(self, uniq_query, error_desc):
        self._callbackError(self, uniq_query, error_desc)
