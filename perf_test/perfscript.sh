#!/bin/bash

rm perf_results.txt
echo "" > perf_results.txt
#pkill -9 python3

FILEPATH=$1
#declare -a SIZES=(4 8 32 64 128 256 512 1024 2048 4096)
#declare -a SIZES=(16384 32768 65536 131072 262144 524288 1048576 2097152 4194304 8388608)
#declare -a SIZES=(16384 32768 65536 131072)
#declare -a SIZES=(4194304)
declare -a SIZES=(1)

echo Regular
for run in {1..100}
do
  echo $run
  for size in ${SIZES[@]}
  do
    #perf stat --append -o perf_results.txt -e cpu-clock python3 $FILEPATH $size
    python3 $FILEPATH >> perf_results.txt
    pkill -9 python3
  done
done

echo Finished!

#python3 perf_parser.py
#python3 db_send.py finalstats.txt $FILEPATH


