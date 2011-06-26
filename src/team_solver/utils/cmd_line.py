"""""
Created on Jun 7, 2011

@author: art_haali
"""""
from team_solver.solvers.process_solver import ProcessSolver
from team_solver.solvers.stp_parser import STPParser
from team_solver.solvers.z3_parser import Z3Parser
from team_solver.solvers.boolector_parser import BoolectorParser


def _create_solvers(ctor, name_prefix, solvers_args):
    cmds_opts = [(sa.split()[0], sa.split()[1:]) for sa in solvers_args]
    return [ProcessSolver(ctor(), name_prefix, a[0], a[1]) for a in cmds_opts]

def create_solvers_from_args(args):
    """ Input: args feeded with add_solvers_args_to_parser function """
    stp_wrappers = _create_solvers(STPParser, "STP", args.stp_solvers)
    z3_wrappers = _create_solvers(Z3Parser, "Z3", args.z3_solvers)
    boolector_wrappers = _create_solvers(BoolectorParser, "Boolector", args.boolector_solvers)
    return stp_wrappers + z3_wrappers + boolector_wrappers

def add_solvers_args_to_parser(parser):
    parser.add_argument('-stp', type=str,
                        dest = "stp_solvers",
                        nargs = "*",
                        default=[],
                        help='add stp solvers (cmds in quotes, separated by space, e.g.: "..../stp --SMTLIB1 -p")')

    parser.add_argument('-z3', type=str,
                        dest = "z3_solvers",
                        nargs = "*",
                        default=[],
                        help='add z3 solvers (cmd in quotes, separated by space, e.g.: "..../z3 -in -smt -m")')

    parser.add_argument('-boolector', type=str,
                        dest = "boolector_solvers",
                        nargs = "*",
                        default=[],
                        help='add boolector solvers (cmd in quotes, separated by space, e.g.: "..../boolector -m -d")')
