import cProfile
import glob
import json
import pstats
from pstats import SortKey
import subprocess
import time
#from numba import jit

#URL = 'https://pypi.org/simple/'
GIT_REPOS = 'repositories.json'
URL_LIST = 'url_list.txt'
REPO_FOLDER = 'repos'

'''
def parse_links(path):
    pattern = re.compile('^ *<a href="(\/simple\/(.*\/))"')
    i = 0
    with open(path) as directory:
        while True:
            line = directory.readline()
            result = pattern.match(line)
            if result is not None:
                url = 'https://pypi.org/simple/' + result.group(2)
                print(url)
                wget.download(url)
'''

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
    counter = 0
    with open(path) as url_file:
        for link in url_file.readlines():
            try:
                print('git clone ' + link[:-1])
                subprocess.run(["git clone " + link[:-1]], shell = True, cwd = 'repos')
            except Exception as e:
                print(e.__doc__)
            time.sleep(10)
            counter += 1
            if counter == 30:
                break

def clean_folders():
    #clean folder rm -rf pyAudioAnalysis
    pass

#@jit
def find_python(repo_folder):
    python_file_list = glob.glob(repo_folder + '/**/*.py', recursive=True)

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

def test_python(python_file_list):
    for file in python_file_list:
        print(file)
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
    test_python(python_file_list)
    

