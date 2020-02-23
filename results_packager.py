from pymongo import MongoClient
from main import RUNS, SIZES
import json
import sys
  
client = MongoClient('mongodb+srv://cluster0-at3ay.gcp.mongodb.net/test',
                      username='preston',
                      password='BnzA7WVQTCVeCdn3',
                      authMechanism='SCRAM-SHA-1')
db = client.mydb

stats_file = sys.argv[1]

with open(stats_file) as stats:
    text = stats.readlines()
    time_list = []
    for line in text:
        time_list.append(json.loads(line))

python_runs = time_list[:RUNS]
numba_runs = time_list[RUNS:]

res = {
      "name": "tsc2.py",
      "sizes": SIZES,
      "runs": RUNS,
      "python": python_runs,
      "numba": numba_runs
}
  
db.stats.insert_one(res)

