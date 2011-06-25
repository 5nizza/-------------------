. ./setup-env.sh


if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` {klee-query}"
  exit $E_BADARGS
fi


./src/team_solver/benchmark_query.py $1 \
-timeout 1 \
-converter "./3rd_party/klee_converter/queries-to-smt-format -print-to-stdout -output-format=smt1 -" \
-stp "./3rd_party/stp/stp --SMTLIB1 -p" \
-boolector "./3rd_party/boolector/boolector --smt -d -m" \
-z3 "./3rd_party/z3/z3 -in -m -smt"

