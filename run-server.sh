. ./setup-env.sh

./src/team_solver/run_server.py -b \
-kleeconverter "/home/art_haali/Documents/eclipse-workspaces/python-workspace/team-solver/queries-to-smt-format -output-format=smt2 -print-to-stdout -optimize-divides=1 -" \
-smtconverter "/home/art_haali//projects/smt-comparison/cvc3-nightly-build-2011-04-01/cvc3-2011-04-01-i686-linux-opt -lang smt2 +translate -output-lang smtlib" \
-stp "/home/art_haali/projects/stp-fast-prover/trunk/stp/bin/stp --SMTLIB1 -p" \
-boolector "/home/art_haali/projects/smt-comparison/boolector-1.4.1-376e6b0-110304/boolector --smt -d -m" \
-z3 "/home/art_haali/projects/smt-comparison/z3/bin/z3 -in -m -smt"
