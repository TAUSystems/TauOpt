""" Functions used in the coordiante descent algorithm """

import numpy as np
from ...config import *
from ...util import checks
import scipy.optimize as scipy_opt

def current_scan_cord(run_info, n):
    """
    Determine the current search direction form "run_info"
    Parameters:
        var_names : list of input parameter names 
        n (int)   : current simulation number
    Returns:
        cord (int): the index of coodinate currently being scanned    
    """
    cord = 0

    if n>1 :
        for m in range(len(config.var_names)):
            if run_info['run'+str(n)][config.var_names[m]] != run_info['run'+str(n-1)][config.var_names[m]] : 
                cord = m
                
    return cord     


def gather_cord_cont_runs(run_info,nmax,cord):
    """
    Gather the values of coordinate varibale and objective function along the scan cordinate "cord"
    
    Prameters:
        run_info (dict) : info. of every run
        nmax (int)      : run_info is read backwards starting from nmax
        cord            : index of the scan cordinate 
    
    Returns:
        pos (numpy.ndarray): 1D array of all values of the coordinate variable
        val (numpy.ndarray): 1D array of the corresponding values of the objection function 
    
    """
    tot = 0
    ind = nmax
    pos = np.zeros(config.max_num_runs)
    val = np.zeros(config.max_num_runs)

    #read "run_info" backward
    while ind>=1:
        
        pos[tot] = run_info['run'+str(ind)][config.var_names[cord]]
        val[tot] = run_info['run'+str(ind)]['opt_fval']
        tot = tot+1
        
        this_cord = current_scan_cord(run_info,ind)
        if this_cord != cord : 
            break
        else: 
            ind = ind-1

    pos = pos[0:tot]
    val = val[0:tot]
    
    return pos,val,ind



def change_scan_cord(sim_num,run_info,cord):
    """
    Change the scan coordinate if the scan along this coordinate axis is complete
    """
    
    pos,val,_ = gather_cord_cont_runs(run_info,sim_num,cord)

    complete,_ = cord_search_converged(pos,val,cord)

    if complete is True : 
        print(f"Cord. Desc. : the search along cord = {cord} converged.\n")       
        #try the next cordiante
        cord = cord +1
        if cord>=len(config.var_names):
            cord = 0
    
    return cord

def cord_search_converged(pos,val,cord):
    """
    Check if the scan along "cord" coordinate axis is complete
    Returns:
        pos_conv (float) : the value of input parameter if coverged
    """
    converged = False
    pos_conv = np.nan

    if len(pos)>=3:

        if checks.nonan_values(val,len(pos)):
        
            if abs(pos[0]-pos[1])<config.var_tolerance[config.var_names[cord]]:
                converged = True
                pos_conv = pos[0]
                #print(f"Search along {cord} converged ! Two consecutive search parameters are within the tolerance. ")
                    
    
    return converged, pos_conv


def max_poly(pos,val,cord):

    var = config.var_names[cord]
    degree = min(4,len(pos)-1)
    neg_val = -val                              
    coeff = np.polyfit(pos, neg_val, degree)

    poly = np.poly1d(coeff)
    
    #res = scipy_opt.minimize_scalar(poly, bounds=(code.var_range[var][0],code.var_range[var][1]), method='bounded')
    #return res.x

    res = scipy_opt.differential_evolution(poly, [( config.var_range[var][0], config.var_range[var][1])], atol= config.var_tolerance[var]*0.01, tol= 0)
    return res.x[0]



