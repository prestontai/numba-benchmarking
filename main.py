import cProfile
from pathlib import Path
import json
import pstats
from pstats import SortKey
import subprocess
import time
import os
import re

import numba_decorator

#URL = 'https://pypi.org/simple/'
GIT_REPOS = 'repositories.json'
URL_LIST = 'url_list.txt'
REPO_FOLDER = 'repos'
BENCHMARK_FOLDER = 'py_files'

def parse_git(repo_list_path, output_path):
    '''
    Parse through the list of git urls provided by
    https://api.github.com/search/repositories?q=library+language:python&sort=stars&order=desc&per_page=500
    '''
    with open(repo_list_path) as repo_file:
        big_dict = json.load(repo_file)['items']
        with open(output_path, 'w+') as output_file:
            for repo in big_dict:
                output_file.write(repo['html_url'] +'\n')
def git_clone(path):
    # there's a library called plotly.py, which is a folder, beware
    counter = 0
    try:
        os.mkdir('repos')
    except:
        pass
    with open(path) as url_file:
        for link in url_file.readlines():
            try:
                print('git clone ' + link[:-1])
                os.chdir('./repos')
                # if folder doesnt exist, git clone it
                if not os.path.isdir(link[:-1].split('/')[-1]):
                    os.system('git clone ' + link[:-1] + '.git')
                    time.sleep(10)
                os.chdir('./..')
            except Exception as e:
                print(e.__doc__)
            counter += 1
            if counter == 30:
                break

def clean_folders():
    #clean folder rm -rf pyAudioAnalysis
    pass

def find_python(repo_folder):
    #python_file_list = glob.glob(r, recursive=True)
    python_file_list = Path(repo_folder).rglob('*.py')
    
    # we want to find the path of several python files from each repo
    repo_names = set()
    python_file_no = 0
    
    condensed_list = []

    for file_path in python_file_list:
        file_path = str(file_path)
        try:
            name = file_path.split('\\')[1]
            if name not in repo_names:
                repo_names.add(name)
                python_file_no = 0
            if python_file_no <= 10:
                condensed_list.append(file_path)
                #print(python_file_list[i])
                python_file_no += 1

            #p = pstats.Stats(python_file_list[i])
            #p.sort_stats(SortKey.TOTTIME).print_stats(10)
            #p.print_stats()
        except Exception as e:
            print(e)
            break
        
    #print(repo_names)
    #print(condensed_list)
    return condensed_list


def test_python(python_file_list, output_folder):
    pattern = re.compile('\\\\')
    for input_file in python_file_list:
        output_file = 'opt-' + re.sub(pattern, '-', input_file)
        os.chdir(output_folder)
        try:
            numba_decorator.run(os.path.join('..', input_file), output_file)
        except:
            pass # go next
        os.chdir('..')
        # profile python file without optimization
        # add optimization
        # profile the new python file that is optimized
        # write the output comparision to a file, but for now print it out
    pass

def compare(file_set):
    pass

if __name__ == "__main__":
    ''' Run parse_git to get an updated list of github links '''
    #parse_git(GIT_REPOS, URL_LIST)
    #git_clone(URL_LIST)
    python_file_list = find_python(REPO_FOLDER)
    test_python(python_file_list, BENCHMARK_FOLDER)
    

