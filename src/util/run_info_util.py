""" Auxilliary functions """
import numpy as np
import sys
from ..config import config

def copy_param(run_info,t,f):
    """
    Copy input parameters in "run_info", from simulation number "t" to simulation number "f"
    
    """
    for v in config.var_names:
        run_info['run'+str(t)][v]=run_info['run'+str(f)][v]

def get_param(run_info,sim_num):
    """
    Returns a dict. of parameters from run_info for Simulation Number sim_num
    
    """ 

    res = {}
    for v in config.var_names:
        res[v] = run_info['run'+str(sim_num)][v]
    
    return res


def insert_param(run_info,sim_num, params):
    """
    Insert input parameters from the dict. "params" to "run_info" for Simulation Number sim_num 
    
    """
    for v in config.var_names:
        run_info['run'+str(sim_num)][v] = params[v]



def get_params_np(run_info,n):
    """ 
    Returns 1D Numpy array of parameters, and the value of obj. func. for Simulation Number n
    """
    
    res = np.full( len(config.var_names), np.nan)
    
    m=0
    for v in config.var_names:
        if  not np.isnan(run_info['run'+str(n)][v]):  
            res[m] = run_info['run'+str(n)][v]
            m=m+1
        else: 
            #return and empty numpy array if any entry in the 'run_info' is NaN
            res = []
            break
    
    fval = run_info['run'+str(n)]['opt_fval']
    return res, fval


def insert_param_np(run_info, sim_num, params):
    """
    Insert input parameters from 1D numpy array to "run_info" for Simulation Number sim_num    
    """
    m=0
    for v in config.var_names:
        run_info['run'+str(sim_num)][v] = params[m]
        m=m+1



class ParamArr:
    
    """
    Restructure parameters stored in 'run_info' into a multidimensional array
    """

    def __init__(self, config, run_info, sim_num):
        
        # number of sample points 
        self.npoints = 0 

    
    def X(self):
        """
        Returns sample points as numpy array
        """
        return self.X
    
    def Y(self):
        """ Return a 1D numpy array of objective function values"""
        return self.Y
    
    
    def insert(self, run_info, sim_num):
        """
        Read and insert parameters from 'run_info'
        """
        
        if sim_num>0:
            
            #initialise the numpy array
            if self.npoints == 0: 
                
                self.X = np.zeros( ( 1, len(config.var_names) ) )
                self.Y = [ np.nan ]
                params, fval = get_params_np(run_info,1)
                
                if len(params) !=0 and not np.isnan(fval): 
                    self.X[0] = params
                    self.npoints = self.npoints + 1
            
            #stack parameters for rest of the simulations
            for n in range(self.npoints+1,sim_num+1):

                params, fval = get_params_np(run_info,n)
                
                if len(params) !=0 and not np.isnan(fval): 
                    self.X = np.vstack(self.X,params)
                    self.Y = np.append(self.Y,fval)
                    self.npoints = self.npoints + 1
            
    
