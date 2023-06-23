""" The coordinate descent algorithm to find optimal input parameters """
from . import cord_desc_plots as plt
from . import cord_desc_utils as utils
from ...config import config 
from ...util import checks
from ...util import run_info_util 
from .model_poly import ModelPoly
import sys
import numpy as np
import random

class CordDesc:


    def __init__(self, vars, sim_num) -> None:

        #index (in config.var_names) of the variable currently being scaned for optimization  
        self.scan_cord_ind = utils.current_scan_cord(vars.run_info, sim_num)
        
        #surrogate model to fit the data
        self.model = ModelPoly(4)


    
    def update_plot(self, run_info, sim_num):
        """
        Make the plot for simumation number "sim_num" showing progress 
        """
        cord = utils.current_scan_cord(run_info, sim_num)
        plt.plot_fval(run_info,sim_num, cord)



    def next_param(self, sim_num, run_info):
        """ Get parameters for simulation number sim_num """

        self.scan_cord_ind = utils.change_scan_cord(sim_num-1,run_info, self.scan_cord_ind)

        if sim_num>1 :
        
            if checks.missing_params(sim_num-1):
                print(f" Err in evaluting parameters for Simulation Number {sim_num}")
                print(f" Inconsistent state : paramters of some prev. simulations are undetermined.")
                sys.exit()
            else:
            

                pos,val,_ = utils.gather_cord_cont_runs(run_info,sim_num-1,self.scan_cord_ind)

                if checks.nonan_values(val,len(pos)):

                    var = config.var_names[self.scan_cord_ind]
                    tol = config.var_tolerance[var]
                    
                    new_pos = self.model.acq_next_param(pos,val, config.var_range[var][0] , config.var_range[var][1], tol )


                    #if the new search point already exists or is too close to the previous point, add some random dispalcement
                    if new_pos in pos or abs(new_pos-pos[0])<tol*0.1:
                        new_pos = new_pos + random.uniform(-0.5, 0.5)*tol 

                    
                    #copy all parameters from previous simulation
                    new_params = run_info_util.get_param_from_run_info(run_info,sim_num-1)
                    new_params[var] = new_pos

                    #copy new parameters for the next simulation
                    run_info_util.insert_param_into_run_info(run_info, sim_num, new_params)




    def converged(self,sim_num, run_info):
        """
        Determine whether the search for optimal input parameters 
        has converged along every axis within the specified tolerance

        """
        
        ind = sim_num
        cord = self.scan_cord_ind
        opt_param = {}
        cord_conv = {}
        nscan = np.zeros(len(config.var_names),dtype=int) 

        #initialize
        for v in config.var_names: 
            opt_param[v] = {}
            cord_conv[v] = False
        
        #read opt. values from mutiple search cycles
        while ind>=1:
            
            pos,val,ind = utils.gather_cord_cont_runs(run_info,ind,cord)
            
            complete, pos_conv = utils.cord_search_converged(pos,val,cord)
            
            #record the opt. value of the parameter, if the search is complete
            if complete:
                opt_param [config.var_names[cord]][nscan[cord]] = pos_conv
                nscan[cord] = nscan[cord] + 1    
            
            #change cordinate    
            cord = cord - 1
            if cord ==-1:
                cord = len(config.var_names)-1
                

        #detemine if all individual cycles have converged
        for v in config.var_names:

            n = len(opt_param[v])

            if n<2:

                cord_conv[v]=False
                #single parameter case
                if n==1 and len(config.var_names)==1:
                    cord_conv[v] = True

            else:    

                if abs(opt_param[v][0] - opt_param[v][1])<config.var_tolerance[v]:
                    cord_conv[v] = True
        



        #determine if all cycles have converged
        res = True
        for v in config.var_names:
            res = res and cord_conv[v]

        
        if res: 
            print(f"Scans along all cordinates have converged. \n")    
        
        return res  


