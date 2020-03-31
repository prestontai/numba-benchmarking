#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
from pymongo import MongoClient
import plotly.graph_objects as go
import os
import json
import numpy as np
from numba import jit

STATS = 'new_stats.txt'

#names = ['python-base', 'numba-base', 'python-intel', 'numba-intel']
client = MongoClient('mongodb+srv://cluster0-at3ay.gcp.mongodb.net/test',
                      username='preston',
                      password='BnzA7WVQTCVeCdn3',
                      authMechanism='SCRAM-SHA-1')
db = client.mydb

names = ['python', 'numba']
def show_graph(size, time_list, runs):
    fig = go.Figure()
    for index, time in enumerate(time_list):
        fig.add_trace(go.Scatter(
            x=size,
            y=time,
            name = names[index],
            connectgaps=True, # override default to connect the gaps
        ))
    fig.update_layout(xaxis_type = 'log',
                      title = 'Runs: ' + str(runs),
                      xaxis_title="size of matrix",
                      yaxis_title="time in seconds",
    )
    fig.show()
    fig.write_html("new_plot.html")

def parse_stats():
    mongo = db.perf.find_one({'name': 'bench_test/s111'})
    size_list = mongo['sizes']
    runs = mongo['runs']
    proc_python = mongo['python']
    proc_numba = mongo['numba']
    '''
    for line, t in enumerate(time_list):
        if line%2 == 0:
            proc_python.append(t)
        else:
            proc_numba.append(t)
    '''
    time_list = [
                 np.mean(proc_python, axis = 0),
                 np.mean(proc_numba, axis = 0)
                ]       
    return size_list, time_list, runs

if __name__ == '__main__':
    clean_args = 'rm ' + STATS
    #os.system(clean_args)
    #os.system('git pull') 
    size, time_list, runs = parse_stats()
    show_graph(size, time_list, runs)
