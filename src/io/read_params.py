""" Basic scan : read parameters for independent simulations from files/functions"""

from ..config import *
import os
import pandas as pd
import h5py

def func_param(sim_num, run_info):
    """
    Get input parameters from a user-defined function
    """
    val = config.func_param(sim_num)
    for n in range(len(config.var_names)): 
        run_info['run'+str(sim_num)][config.var_names[n]]=val[n]   


def read_param_from_file(sim_num,run_info):
    """
    Read input parameters from a file
    """
    f=config.project_folder+'/'+config.var_filename
    
    if not os.path.exists(f):
        sys.exit("The parameter file (values of 'var_names') could not be found")

    ext = os.path.splitext(config.var_filename)[1]

    #read paramters from an hdf5 file
    if ext == '.h5' or ext == '.hdf5':

        data = h5py.File(f,'r')
        for v in config.var_names:
            run_info['run'+str(sim_num)][v]=data[v][sim_num-1]
    
    # read parameters from an excel file
    elif ext == '.xls' or ext=='.xlsx':
        df = pd.read_excel(f)
        alter_num_runs(df.shape[0])
        if sim_num <=df.shape[0]:
            data = df.iloc[sim_num-1]
            for v in config.var_names:
                run_info['run'+str(sim_num)][v]=data[v]

    
    # read parameters from a csv/text file, the first line must be header
    elif ext == '.csv' or ext =='.txt':
        with open(f) as param_file:
            line = param_file.readlines()
            alter_num_runs(len(line)-1)
            if sim_num<len(line):
                fields = line[sim_num].strip().split(',')
                n=0
                for v in config.var_names:
                    run_info['run'+str(sim_num)][v] = float(fields[n])
                    n = n+1

    else:
        sys.exit("The parameter file could not be read. Format not supported.")



def alter_num_runs(num):
    """
    Update the max. num. of simulations in the configuration file
    """
    if num != config.max_num_runs:
        config.max_num_runs = num 