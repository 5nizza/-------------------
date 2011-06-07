. ./setup-env.sh


if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` {klee-query}"
  exit $E_BADARGS
fi


./src/team_solver/benchmark_query.py $1 \
-timeout 0.1 \
-converter "/home/art_haali/projects/pure-klee/Release+Asserts/bin/queries-to-smt-format -print-to-stdout -output-format=smt1 -" \
-stp "/home/art_haali/projects/stp-fast-prover/trunk/stp/bin/stp --SMTLIB1 -p" \
-boolector "/home/art_haali/projects/smt-comparison/boolector-1.4.1-376e6b0-110304/boolector --smt -d -m" \
-z3 "/home/art_haali/projects/smt-comparison/z3/bin/z3 -in -m -smt"

