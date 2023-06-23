""" Auxilliary functions """

from ..config import config

def copy_param(run_info,t,f):
    """
    Copy input parameters in "run_info", from simulation number "t" to simulation number "f"
    
    """
    for v in config.var_names:
        run_info['run'+str(t)][v]=run_info['run'+str(f)][v]

def get_param_from_run_info(run_info,sim_num):
    """
    Returns a dict. of parameters from run_info for Simulation Number sim_num
    
    """ 

    res = {}
    for v in config.var_names:
        res[v] = run_info['run'+str(sim_num)][v]
    
    return res


def insert_param_into_run_info(run_info,sim_num, params):
    """
    Insert input parameters from the dict. "params" to "run_info" for Simulation Number sim_num 
    
    """
    for v in config.var_names:
        run_info['run'+str(sim_num)][v] = params[v]
    

