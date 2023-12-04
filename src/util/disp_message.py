""" Display messages in terminal """

import numpy as np
from ..config import config

def disp_best_sim_params(sim_num, run_info):
    """
    Show info. from the simulation with max. value of the objective function
    """
    pos = np.zeros(sim_num)
    val = np.zeros(sim_num)
    
    for n in range(1,sim_num+1):
        pos[n-1] = n
        val[n-1] = run_info['run'+str(n)]['opt_fval']
    
    max_val_ind = np.argmax(val)

    print(f"Max. value ( {val[max_val_ind]} ) found in Run Number :  {max_val_ind+1}")

    #print the values of parameters
    for v in config.var_names:
        print(f"{v} : {run_info['run'+str(max_val_ind+1)][v]} ")
