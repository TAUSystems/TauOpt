""" The coordinate descent algorithm to find optimal input parameters """
from . import cord_desc_plots as plt
from . import cord_desc_scans as utils
from ...config import config
from ...util import checks
from ...util import run_info_util 
from ..models.model_poly import ModelPoly
from ..models.model_gp import ModelGP
import sys
import numpy as np
import random

class CordDesc:


    def __init__(self, vars, sim_num) -> None:

        #index (in config.var_names) of the variable currently being scaned for optimization  
        self.model = {}
        self.scans = utils.ScanSequence()

        #load data in "scans" from run_info 
        for n in range(1,sim_num+1):
            self.scans.append(vars.run_info, n)
            self.scans.cord_scan[ self.scans.nscan ].update_pos_val(vars.run_info)
            self.scans.change_scan_cord(vars.run_info)
        

        #select a surrogate model to fit the data for each axis
        for v in config.var_names:
            
            #polynomial model is the default, see config.py
            if config.opt_algo_config['model'] == 'poly':
                self.model[v] = ModelPoly(config.model_poly_config['max_deg']) 

            #Guassian process 
            if config.opt_algo_config['model'] == 'gp':
                self.model[v] = ModelGP() 





    
    def update_plot(self, run_info, sim_num):
        """
        Make the plot for simumation number "sim_num" showing the progress 
        """
        cord = self.scans.current_scan_cord
        plt.plot_fval(run_info, sim_num, self.scans, self.model[config.var_names[cord]])



    def next_param(self, sim_num, run_info):
        """ Get parameters for Simulation Number sim_num """

        #update pos, val in "scans" from run_info  
        self.scans.cord_scan[ self.scans.nscan ].update_pos_val(run_info)   

        #detemine if the curren scan is complete, if yes, then move to the next coordinate
        self.scans.change_scan_cord(run_info)   
        
        if sim_num>1 :
        
            if checks.missing_params(sim_num-1):
                print(f" Err in evaluting parameters for Simulation Number {sim_num}")
                print(f" Inconsistent state : paramters of some prev. simulations are undetermined.")
                sys.exit()
            else:
            
                pos, val = self.scans.pos_val_from_current_scan() 

                if checks.nonan_values(val,len(pos)):

                    var = config.var_names[ self.scans.current_scan_cord ]
                    tol = [ config.var_tolerance[var] ]
                    bounds = [ (config.var_range[var][0], config.var_range[var][1] ) ]
                    
                    if len(pos) < config.opt_algo_config['num_warm_points']:
                        new_pos = self.warm_start_pos(pos, bounds)
                    else:
                        if config.opt_algo_config['model'] == 'poly':
                            new_pos = self.model[var].acq_next_param(pos,val, bounds , tol )
                        
                        if config.opt_algo_config['model'] == 'gp':
                            pos_gp = pos.reshape(-1,1)
                            val_gp = val.reshape(-1,1)
                            new_pos = self.model[var].acq_next_param(pos_gp, val_gp, bounds , tol)
                            new_pos = new_pos[0]


                    #if the new search point already exists or is too close to the previous point, add some random dispalcement
                    new_pos = self._well_seprated_next_param(new_pos, pos, tol[0], bounds)

                    
                    #copy all parameters from previous simulation
                    new_params = run_info_util.get_param( run_info, sim_num-1 )
                    new_params[var] = new_pos

                    print(new_params)

                    #copy new parameters for the next simulation
                    run_info_util.insert_param(run_info, sim_num, new_params)
                    self.scans.append(run_info, sim_num)

        #the first simulation uses the initial values val0 
        else:
            # include the run id in "scan"
            self.scans.append(run_info, sim_num)



    def _well_seprated_next_param(self, pos0, pos, tol, bounds):
        """
        suggested position "new_pos" is passed though the closeness test, i.e., 
        if "new_pos" is too close to an already explored point and some random dispalcement 
        is added to make sure that the points are well seperated. 
        """
        
        new_pos = pos0
        
        n=1 
        while np.min(np.abs(new_pos-pos)) < 0.01*tol:
            
            new_pos = new_pos + random.uniform(-0.5, 0.5)*tol

            new_pos = self._map_within_bounds(new_pos, bounds)
            
            #make sure that the loop is terminated
            n=n+1
            if n == 1000: 
                print(f" Warning : could not find well-seprated parameters for the next evaluation! ")
                break


        return new_pos
    

    
    def warm_start_pos(self, pos, bounds):
        """
        The first few points before using the surrogate model 
        to predict the next position
        """

        lb = bounds[0][0]
        rb = bounds[0][1]

        diff = (rb - lb)/config.opt_algo_config['num_warm_points']
        n = len(pos)

        next_pos = pos[0] + 0.5*diff + (n-1)*diff + random.uniform(-0.5, 0.5)*diff
        
        next_pos = self._map_within_bounds(next_pos, bounds)
        
        return next_pos
    

    
    def _map_within_bounds(self, p, bounds):
        """
        make sure that the point "p" is well within the bounds
        """

        lb = bounds[0][0]
        rb = bounds[0][1]

        if p > rb: 
            p = lb + (p - rb)
            
        if p < lb:
            p = rb - (lb - p)
        
        return p



    def converged(self, sim_num, run_info):
        """
        Determine whether the search for optimal input parameters 
        has converged along every axis within the specified tolerance
        """
        
        opt_param = {}
        cord_conv = {}
        nscan = np.zeros(len(config.var_names),dtype=int) 

        #initialize
        for v in config.var_names: 
            opt_param[v] = {}
            cord_conv[v] = False
        
        #read opt. values from mutiple search cycles
        for n in range(1,self.scans.nscan+1):
            
            pos = self.scans.cord_scan[n].pos 
            val = self.scans.cord_scan[n].val 
            cord = self.scans.cord_scan[n].cord

            complete = self.scans.cord_scan[n].complete()
            
            #record the opt. value of the parameter, if the search is complete
            if complete:
                opt_param [config.var_names[cord]][nscan[cord]] = self.scans.cord_scan[n].pos_best
                nscan[cord] = nscan[cord] + 1    
            
                

        #determine if all individual cycles have converged
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
