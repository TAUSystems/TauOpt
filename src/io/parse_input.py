""" Methods for processing user inputs """

import os

def user_config_file_name(str_in):
    """ extract python file name (config file) from the input string  """
    
    str_in = str_in.split(".")[0].lstrip('-').strip()

    _, fname_parsed = os.path.split(str_in)
    
    fname_parsed = fname_parsed+'.py'
    path_parsed = str_in+'.py'

    if not os.path.isfile(path_parsed):
        print(f" The configuration file could not be found ! ")
        print(f" Please prodive a correct full path (with the script name) as an argument to TauOpt.py. ")
        print(f" Example: python3 TauOpt.py /Users/Project/my_config.py use \\ for Win Os  \n ")
        print(f" The path you provided : {path_parsed} ")
    
    return fname_parsed, path_parsed