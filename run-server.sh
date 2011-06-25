. ./setup-env.sh

./src/team_solver/run_server.py \
-kleeconverter "./3rd_party/klee_converter/queries-to-smt-format -output-format=smt2 -print-to-stdout -optimize-divides=1 -" \
-smtconverter "./3rd_party/smt_converter/cvc3-2011-04-01-i686-linux-opt -lang smt2 +translate -output-lang smtlib" \
-stp "./3rd_party/stp/stp --SMTLIB1 -p" \
-z3 "./3rd_party/z3/z3 -in -m -smt" \
-boolector "./3rd_party/boolector/boolector --smt -d -m" 
