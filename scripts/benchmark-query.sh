. $(dirname $0)/setup-env.sh


if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` {klee-query}"
  exit $E_BADARGS
fi


$TEAM_SOLVER_ROOT/src/team_solver/benchmark_query.py $1 \
-timeout 10 \
-kleeconverter "$TEAM_SOLVER_ROOT/3rd_party/klee_converter/queries-to-smt-format -output-format=smt2 -print-to-stdout -optimize-divides=1 -" \
-smtconverter "$TEAM_SOLVER_ROOT/3rd_party/smt_converter/cvc3-2011-04-01-i686-linux-opt -lang smt2 +translate -output-lang smtlib" \
-stp "$TEAM_SOLVER_ROOT/3rd_party/stp/stp --SMTLIB1 -p -t" \
-boolector "$TEAM_SOLVER_ROOT/3rd_party/boolector/boolector --smt -d -m -v -v" \
-z3 "$TEAM_SOLVER_ROOT/3rd_party/z3/z3 -in -m -smt -st"

