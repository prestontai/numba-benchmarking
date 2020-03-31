from pymongo import MongoClient
import json
import sys
 
RUNS = 10
SIZES = [16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608]
client = MongoClient('mongodb+srv://cluster0-at3ay.gcp.mongodb.net/test',
                      username='preston',
                      password='BnzA7WVQTCVeCdn3',
                      authMechanism='SCRAM-SHA-1')
db = client.mydb

stats_file, test_file = sys.argv[1], sys.argv[2]

with open(stats_file) as stats:
    text = stats.readlines()
    time_list = []
    for line in text:
        time_list.append(json.loads(line))

python_runs = time_list[:RUNS]
numba_runs = time_list[RUNS:]

res = {
      "name": test_file,
      "sizes": SIZES,
      "runs": RUNS,
      "python": python_runs,
      "numba": numba_runs
}
 
db.perf.insert_one(res)
