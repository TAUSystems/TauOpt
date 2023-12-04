"""
Runtime checks
"""

from ..config import config
from ..util import gbl_vars
import numpy as np
import sys
from ..run_sim import sim_status
from ..opt_algos import opt_algo as opt

def valid_param(sim_num):
    valid = True
    for v in config.var_names:
        if np.isnan(gbl_vars.run_info['run'+str(sim_num)][v]):
            valid = False
        else:
            if config.scan_type=='opt':
                if gbl_vars.run_info['run'+str(sim_num)][v] < config.var_range[v][0] or gbl_vars.run_info['run'+str(sim_num)][v] > config.var_range[v][1]:
                    valid = False
    
    rep = repeated_param(sim_num)
    if rep>0:
        print(f"Err: parameters for sim. num. {sim_num} are the same as in sim. num. {rep}")
        sys.exit("Exiting..... ")
    
    return valid

def repeated_param(sim_num):
    """
    Compare parameters for sumulation number "sim_num" with all previous simulations
    Returns:
        res (bool) : True, if a match is found
    """
    res = 0
    for n in range(1,sim_num):
        repeat = True
        for v in config.var_names:
            if gbl_vars.run_info['run'+str(n)][v] != gbl_vars.run_info['run'+str(sim_num)][v]:
                repeat = False
                break

        if repeat == True:
            print(f"parameters for run {sim_num} is same as in run {n}")
            res = n
            break
    
    return res

def missing_params(sim_num):
    """
    Check if the input parameters of previous simulations are missing from "run_info" 
    """
    missing = False
    for n in range(1,sim_num+1):
        present_this = False 
        for v in config.var_names:
            if not np.isnan( gbl_vars.run_info['run'+str(n)][v]):
                present_this = True
            
        if present_this is False: 
            print(f"sim no. {sim_num} : missing params for run {n}")
            missing = True
        
    return missing

def nonan_values(val,nval):
    valid = True
    for n in range(nval):
        if np.isnan(val[n]): 
            valid = False
        
    return valid



def all_complete(sim_num,run_info):
    """
    Check if all tasks finished in accordance with current configuration
    Returns:
        res (bool) : True, if all tasks completed
    
    """
    res = False
    if sim_num >= config.max_num_runs:
        if all_sim_finished(sim_num):
            res = True

    #check if the optimization search has converged    
    if config.scan_type=='opt':
        if opt.converged(sim_num, run_info):
            res = True

    return res


def all_sim_finished(sim_num):
    """
    Check if all simulations with number up to "sim_num" have finished
    """
    res = True
    for n in range(1,sim_num+1):
        if not sim_status.sim_finished(n):
            res = False
            break

    return res

def all_status_check(sim_num):
    """
    Check status of every unfinished simulation 
    """
    for n in range(1,sim_num+1):
        sim_status.check_sim_status(n)

def within_tolerance(params1, params2):
    """
    Check if params 1 and 2 are within the tolerance
    """
    res = True

    try:
        for v in config.var_names:
            if abs(params1[v]-params2[v])>config.var_tolerance[v]:
                res = False
    except: 
        res = False
    
    return res
