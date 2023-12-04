""" Optimization algorithms """
from ..run_sim import sim_status
from .cord_desc.cord_desc_algo import CordDesc
from .bayesian.bayesian_algo import BayesianOptimization
import numpy as np
from ..config import *
from ..run_sim import *
from ..util import gbl_vars
from ..io import load_data
import os
import time

#plotting is complete for all runs with "num" lower than this 
plotting_completed = 0



def init(config, vars, sim_num):
    """
    Initialise configuration/variables for the chosen algorithm 

    Parameters: 
        config          :  
        vars            : all global varaibles
        sim_num (int)   : current simulation number

    """
    if config.opt_algo_config['type'] == 'cord_desc':
        gbl_vars.algo = CordDesc(vars, sim_num)
    
    if config.opt_algo_config['type'] == 'bayesian':
        gbl_vars.algo = BayesianOptimization(vars, sim_num)
    

    update_run_info(sim_num,vars.run_info) 

   
def get_param(sim_num, run_info):
    """ Get parameters for simulation number sum_num """
    
    gbl_vars.algo.next_param(sim_num, run_info)


def converged(sim_num, run_info):
    """
    Determine if the optimization has converged
    """
    res = False
    if gbl_vars.algo.converged(sim_num, run_info):
        res = True
        
    
    return res


def update_run_info(sim_num,run_info):
    """
    Update all necessary quantities in run_info filled in by the optimization algorithms
    """

    #update the values of objective function
    update_val_obj_func(sim_num,run_info)

    #update all plots produced by the optimization scheme
    update_plots(sim_num, run_info)



def update_plots(sim_num,run_info):
    """
    Update all plots produced by the optimization algorithm
    """
    for n in range(1 , sim_num+1):
        if make_plot(run_info,n):
            gbl_vars.algo.update_plot(run_info, n)
            run_info['run'+str(n)]['plotted'] = True 






def update_val_obj_func(sim_num,run_info):
    """
    Fill in the updated values of objective function (if available and not updated) into "run_info"
    """
    for m in range(1,sim_num+1):
        if np.isnan(run_info['run'+str(m)]['opt_fval']): 
            run_info['run'+str(m)]['opt_fval'] = val_obj_func(m)


def val_obj_func(sim_num):
    """
    Value of the objective function for the simulation number "sim_num"
    Parameter:
        sim_num (int) : simulation number
    Returns:
        val (float)   : value of the objective function

    """
    val = np.nan  
    f = config.project_folder+'/'+'run'+str(sim_num)+'/tau_opt/opt_fval.txt'
    
    #read value from previous evalaution, saved in a file
    if os.path.isfile(f):
        val = load_data.read_num_from_file(f)

    
    else:
        if sim_status.sim_finished(sim_num): 
            # wait, just in case the file is still being written from previous run
            time.sleep(10) 
            
            os.chdir(config.project_folder+'/'+'run'+str(sim_num))
            
            #call the user-defined objective func. from the run directory
            if callable(config.objective_function):
                val = config.objective_function()
            
            #read the value directly from the output file written by simulation code
            elif isinstance(config.objective_function, str):
                val = load_data.read_num_from_file(config.project_folder+'/'+'run'+str(sim_num)+'/'+config.objective_function)

            os.chdir(config.project_folder)

            #write the value in a file
            print(f"The value of objective function for simulation number {sim_num} is: {val}")
            with open(f,'w') as file:
                file.write(str(val))
        
        else:
            
            print(f"Can't evaluate the objective function ! Simulation Number {sim_num} has not finished yet !!")
            sim_status.check_sim_status(sim_num)
             

    return val



def make_plot(run_info,sim_num):
    """
    Determine whether the plot can/should be produced for the simulation number "sim_num"
    
    Returns: 
        res (bool) : True, if plots can/should be produced
    
    """
    res = False

    #Make plot, if the plot does not already exist
    if not run_info['run'+str(sim_num)]['plotted']:
        res = True
        for n in range(1,sim_num+1):
            
            #plots can't be produced if the objective function doesn't yet have a valid value
            if np.isnan(run_info['run'+str(n)]['opt_fval']):
                res = False
            

    return res

