""" Read data from files """

from ..config import *
import os
import json

def load_param(sim_num,run_info):
    if not os.path.isfile(config.project_folder+'/'+'run'+str(sim_num)+"/tau_opt/param.json"):
        sys.exit(f"Error: JSON file for the parameters not found for sim_num = {sim_num}! ")

    with open(config.project_folder+'/'+'run'+str(sim_num)+"/tau_opt/param.json","r") as f:
        param = json.load(f)
    
    for v in config.var_names:
        run_info['run'+str(sim_num)][v] = param[v]
    


def read_num_from_file(filename):
    
    with open(filename,'r') as file:
        content = file.read().strip()
        print(content)
        try:
            number = int( content )
            return number
        except ValueError:
            try:
                number = float ( content )
                return number
            except ValueError:
                print(f"Could not read output from {filename}")
