#!/bin/bash

#USAGE EX: ./smartscript.sh bench_test/s111 500000

./clean.h
rm perf_results1.txt
rm perf_results2.txt
echo "" > perf_results1.txt
echo "" > perf_results2.txt

FILEPATH=$1
#"bench_test/s111"
REGULAR="$FILEPATH.py"
OPT="$FILEPATH"opt.py
#declare -a SIZES=(4 8 32 64 128 256 512 1024 2048 4096)
SIZE=$2
#declare -a SIZES=(16384 32768 65536 131072 262144 524288 1048576 2097152 4194304 8388608)
#declare -a SIZES=(16384 32768 65536 131072)
#declare -a SIZES=(4194304)

echo Regular
perf stat --append -o perf_results1.txt -e cpu-clock python3 $REGULAR $SIZE

echo Numba
python3 numba_decorator.py $REGULAR $OPT 
# This is the first run to cache results
python3 $OPT 10 > /dev/null
perf stat --append -o perf_results2.txt -e cpu-clock python3 $OPT $SIZE

echo Finished!

python3 smart_parser.py
#python3 smart_runner.py $REGULAR $OPT finalstats.txt

