import plotly.graph_objects as go
import os
import json

names = ['python-base', 'numba-base', 'python-intel', 'numba-intel']
def show_graph(size, time_list):
    fig = go.Figure()

    for index, time in enumerate(time_list):
        fig.add_trace(go.Scatter(
            x=size,
            y=time,
            name = names[index],
            connectgaps=True, # override default to connect the gaps
        ))
    fig.update_layout(xaxis_type = 'log')
    fig.show()

def parse_stats(path):
    with open(path) as stats:
        s = stats.readlines()
    size = json.loads(s[0])
    time_list = []
    for s in s[1:]:
        time_list.append(json.loads(s))

    return size, time_list

if __name__ == '__main__':
    os.system('git pull') 
    size, time_list = parse_stats('stats.txt')
    show_graph(size, time_list)
