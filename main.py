#!/usr/bin/python3
import cProfile
from pathlib import Path
import glob
import json
import pstats
import subprocess
import time
import os
import re
import sys
import subprocess

import numba_decorator

#URL = 'https://pypi.org/simple/'
#GIT_REPOS = 'repositories.json'
URL_LIST = 'url_list.txt'
REPO_FOLDER = 'bench_test'
BENCHMARK_FOLDER = 'py_files'
BREAKPOINT = 10
TIMEOUT = 25
SIZES = [100, 1000, 10000, 100000]
ANALYTICS = 'stats.txt'

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
    python_file_list = glob.glob(repo_folder + '/**/*.py', recursive=True)
    #python_file_list = Path(repo_folder).rglob('*.py')
    #python_file_list = [str(p) for p in python_file_list if 'opt' not in str(p)]
    
    # we want to find the path of several python files from each repo
    repo_names = set()
    python_file_no = 0
    
    condensed_list = []

    for file_path in python_file_list:
        try:
            name = file_path.split('/')[1]
            if name not in repo_names:
                repo_names.add(name)
                python_file_no = 0
            if python_file_no <= 10 and 'opt' not in file_path:
                condensed_list.append(file_path)
                python_file_no += 1

        except Exception as e:
            print(e)
            break
    return condensed_list

def profile_stats(script, muted = False):
    #os.system('python3 -m cProfile -o 0.txt ' + input_file)
    
    times = []
    for s in SIZES:
        args = 'vtune -c hotspots -report summary python3 ' + script + ' ' + str(s)
        try:
            if muted:
                proc = subprocess.run(args, shell = True,
                    stderr = subprocess.DEVNULL,
                    stdout = subprocess.DEVNULL,
                    timeout = TIMEOUT)
                break
            else:
                proc = subprocess.run(args, shell = True, timeout = TIMEOUT)
                #parse vtune data and append to times
        except subprocess.TimeoutExpired:
            print('process took too long')
    
    with open(ANALYTICS, 'w+') as stats:
        stats.write(str(SIZES))
        #stats.write(
    #os.system('vtune -c hotspots -report summary -report-knob show-issues=false python3 ' + script + redirection)
    
    '''
    # make it so it ends up going to an actual readable output.
    # i need to compare them too
    with open('1.txt', 'w+') as out:
        p = pstats.Stats('0.txt', stream = out)
        p.strip_dirs().sort_stats('tottime').print_stats(10)

    with open('1.txt', 'r') as out:
        summary = out.readlines()[2]
    pattern = re.compile('[\d]+\.[\d]+')
    return re.search(pattern, summary).group(0)
    '''
    
def test_python(python_file_list):
    # profile python file without optimization
    # add optimization
    # profile the new python file that is optimized
    # write the output comparision to a file, but for now print it out
    for counter, input_file in enumerate(python_file_list):
        try:
            profile_stats(input_file)
            output_file = input_file[:-3] + 'opt.py'
            try:
                numba_decorator.run(input_file, output_file)
                
                # This is run once first so it creates a cache.
                profile_stats(output_file, True)
                # This is uses the precompiled code.
                profile_stats(output_file)
            except Exception as e:
                print(e) #go next
        except Exception as e:
            print(e)
        print()
        
        # I want to test a small amount first.
        if counter > BREAKPOINT:
            break

def compare(file_set):
    pass

if __name__ == "__main__":
    ''' Run parse_git to get an updated list of github links '''
    #parse_git(GIT_REPOS, URL_LIST)
    #git_clone(URL_LIST)
    python_file_list = find_python(REPO_FOLDER)
    test_python(python_file_list)
    
