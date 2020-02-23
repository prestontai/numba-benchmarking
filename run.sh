#!/bin/bash
./clean.sh
rm stats.txt
rm results.txt
pkill -9 python3
python3 main.py >> results.txt
python3 vtune_parser.py newnewstats.txt
python3 result_packager.py newnewstats.txt
