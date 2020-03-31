#!/bin/bash

./clean.sh
rm justopt.txt
rm finalstats.txt
rm perf_results1.txt
rm perf_results2.txt
echo "" > perf_results1.txt
echo "" > perf_results2.txt
#pkill -9 python3

FILEPATH=$1
#"bench_test/s111"
REGULAR="$FILEPATH.py"
OPT="$FILEPATH"opt.py
#declare -a SIZES=(4 8 32 64 128 256 512 1024 2048 4096)
declare -a SIZES=(16384 32768 65536 131072 262144 524288 1048576 2097152 4194304 8388608)
#declare -a SIZES=(16384 32768 65536 131072)
#declare -a SIZES=(4194304)

echo Regular
for run in {1..10}
do
  for size in ${SIZES[@]}
  do
    perf stat --append -o perf_results1.txt -e cpu-clock python3 $REGULAR $size
    pkill -9 python3
  done
  echo $run
done

echo Numba

python3 numba_decorator.py $REGULAR $OPT

# This is the first run to cache results
python3 $OPT 1000

for run in {1..10}
do
  for size in ${SIZES[@]}
  do
    perf stat --append -o perf_results2.txt -e cpu-clock python3 $OPT $size
    pkill -9 python3
  done
  echo $run
done

echo Finished!

python3 perf_parser.py
python3 db_send.py finalstats.txt $FILEPATH


