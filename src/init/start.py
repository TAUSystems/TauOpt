""" Start TauOpt """
import sys
import numpy as np
import os

from src import opt_algos
from ..io import load_data
from ..util import *
from ..io import *
from ..opt_algos import opt_algo

def startup_message():
    """ message displayed at the start """

    show_TAU_logo()

    print(f" TauOpt started at : {fmt.get_time()} \n")

def init_complete_message():
     print(f"Initializations complete ! \n")


def init(config, vars, sim_num):
    """ 
    
    Initialise all internal variables.    
    Reload info. any previous runs.
    Setup the optimization algorithm. 

    Prameters: 
        config        : configuration module
        vars          : global internal varaibles
        sim_num (int) : current simulation number 
    
    """

    #display important details about the current configuration state 
    show_fyi()
    
    #initialize the entire "run_info" dictionary
    for n in range(1,config.max_num_runs+1):
         vars.run_info['run'+str(n)]={}
         vars.run_info['run'+str(n)]['opt_fval'] = np.nan
         vars.run_info['run'+str(n)]['plotted'] = False
         for v in config.var_names:
             vars.run_info['run'+str(n)][v]=np.nan
    
    #The very first simulations uses the set of intial parameters, if configured
    if len(config.var_val0) !=0 :
        for n in range(len(config.var_names)):
            vars.run_info['run1'][config.var_names[n]] = config.var_val0[n]
    
    #set existing values of the function to be optimized
    if config.scan_type=='opt':
        for n in range(1,sim_num+1):
            os.chdir(config.project_folder+'/run'+str(n))
            vars.run_info['run'+str(n)]['opt_fval'] = opt_algo.val_obj_func(n)
            os.chdir(config.project_folder)
    
            
    #load values of the input paramters from existing runs 
    if sim_num>0:
        print(f"Gathering info. from {sim_num} previous simulations. \n")


    for n in range(2,sim_num+1):
        param_file = config.project_folder+'/run'+str(n)+'/tau_opt/param.json'
        if os.path.exists(param_file):
            load_data.load_param(n,run_info)
        else:
            sys.exit(f" Parameter file for Simulation Number {n} could not be found.")  

   
    #initialize the optimization algorithm 
    if config.scan_type == 'opt':
        opt_algos.init(config, vars, sim_num)           

def show_fyi():
    """ 
    Display some messages that inform users regarding the default behavior and how TauOpt has been configured
    """
    if os.path.isfile(config.project_folder+'/'+config.code_name+'/'+config.exec_name):
        print(f"Executable already exists in the code folder, so compilation will not be attempted.") 
        print(f"Only the executable, input files, and auxilary files (if any) will be copied between runs.")





def show_TAU_logo():
    """
    Display the logo of " Tau Systems Inc."
    """
    with open('src/init/TAU_logo.txt','r') as file:
        content = file.read()
        print(content)
