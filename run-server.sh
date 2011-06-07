. ./setup-env.sh

./src/team_solver/run_server.py -b \
-stp "/home/art_haali/projects/stp-fast-prover/trunk/stp/bin/stp --SMTLIB1 -p" \
-boolector "/home/art_haali/projects/smt-comparison/boolector-1.4.1-376e6b0-110304/boolector --smt -d -m" \
-z3 "/home/art_haali/projects/smt-comparison/z3/bin/z3 -in -m -smt"
