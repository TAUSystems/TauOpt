""" The Bayesian Optimization Algorithm """

from ...config import config
from ...util.run_info_util import ParamArr, insert_param_np
from ...util import gbl_vars as gbl
import numpy as np
from ..models.model_gp import ModelGP


class BayesianOptimization:

    def __init__(self, vars, sim_num) -> None:
        self.params = ParamArr( vars.run_info, sim_num) #returns input paramters as Numpy array 
        self.model = ModelGP() #Default model : Gaussian Process  
    
    def next_param(self, sim_num, run_info):
        """ Get parameters for simulation number 'sim_num' """

        #make sure that the numpy array of sample points is up to date
        self.params.insert(run_info, sim_num)
        
        if sim_num>1 :
            
            pos_next = self.model.acq_next_param(self.params.X(),self.params.Y(), gbl.bounds  , gbl.tol )

            insert_param_np(run_info, sim_num, pos_next)


    def update_plot(self, run_info, sim_num):
        pass
        
    
    def converged(self, n , run_info):
        """
        Determined whether the search has converged or not
        """
        res = False
        
        if n>np.max(2,len(config.var_names)):
            
            res = True
            for v in config.var_names:
                if np.abs(run_info[n][v] - run_info[n-1][v])>config.var_tolerance[v]:
                    res = False
                    break
        
        return res