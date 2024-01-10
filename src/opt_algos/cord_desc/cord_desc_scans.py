""" Functions used in the coordiante descent algorithm """

import numpy as np
from ...config import *
from ...util import checks
import scipy.optimize as scipy_opt

class ScanSequence:

    def __init__(self) -> None:

        self.current_scan_cord = 0 # index of the coordinate currenly being scanned
        
        self.cord_scan = {} #CordScan objects for every scan along individual coordiantes  
        
        self.nscan = 1 # total number of scans
        self.cord_scan[1] = CordScan(0) 
    
    def change_scan_cord(self, run_info):
        """
        Change the scanning coordinate if the current scan is complete
        """
        complete = self.cord_scan[self.nscan].complete()

        if complete: 
            print(f"Cord. Desc. : the search along cord = {self.current_scan_cord} is complete.\n")       
            
            #scan the next coordiante
            self.current_scan_cord = self.current_scan_cord +1
            if self.current_scan_cord>=len(config.var_names):
                self.current_scan_cord = 0
            
            #create a new CordScan object for the next scan
            self.nscan = self.nscan +1 
            self.cord_scan[self.nscan] = CordScan(self.current_scan_cord)
            
            #start the next scan from the best obs. point in the previous scan
            if self.nscan>1:
                self.append( run_info, self.cord_scan[ self.nscan-1 ].run_id_best )
                self.cord_scan[self.nscan].update_pos_val(run_info)


    def append(self, run_info, n):
        """
        Include a new simulation (index n in run_info) into the list for the cord. scan
        update pos, val from run_info 
        """
        self.cord_scan[self.nscan].insert(n)
        
        
    
    def pos_val_from_current_scan(self):
        """
        Returns position (pos) and values (val) from the current coodinate scan
        """

        pos = self.cord_scan[self.nscan].pos 
        val = self.cord_scan[self.nscan].val

        return pos, val
        

class CordScan:

    def __init__(self, cord ) -> None:
        self.run_id = np.array([], dtype=int)
        self.cord = cord
        
        #position and values of the objective function for this scan 
        self.pos = []
        self.val = []

        #run_id for the best observed value
        self.pos_best = np.nan
        self.val_best = np.nan
        self.run_id_best = np.nan

    
    def insert(self, id):
        """
        Include a new simulation (index n in run_info) into the list (run_id) for this scan
        """

        if not np.isin(id, self.run_id):
            self.run_id = np.append(self.run_id, id)
    
    
    def update_pos_val(self, run_info):
        """
        Update the values of coordinate varibale and objective function along the scan cordinate "cord"
        
        Prameters:
            run_info (dict) : info. of every run
                
        """

        num_runs = len(self.run_id)
        self.pos = np.zeros(num_runs)
        self.val = np.zeros(num_runs)

        for n in range(len(self.run_id)):
            id = self.run_id[n]
            self.pos[n] = run_info['run'+str(id)][config.var_names[self.cord]]
            self.val[n] = run_info['run'+str(id)]['opt_fval']
        
    

    
    def complete(self):
        """
        Check if the scan along "cord" coordinate axis is complete
        Returns:
            complete (boolean) : True if coverged/complete
        """

        complete = False

        #places where the values of obj. func. is not nan
        ind_nonan = np.where(~np.isnan(self.val))[0]

        if ind_nonan.size > 0 : 

            #get non-nan values from "val" and correspoding "pos"
            pos_nonan = self.pos[ind_nonan]
            val_nonan = self.val[ind_nonan]
            id_nonan  = self.run_id[ind_nonan]
                    
            #sort the values of obj. func.  
            ind_sorted = np.argsort(val_nonan)
            val_sorted = val_nonan[ind_sorted]
            pos_sorted = pos_nonan[ind_sorted]
            id_sorted  = id_nonan[ind_sorted]
            print(pos_sorted)
 
            #best obeserved so far
            self.pos_best = pos_sorted[-1]
            self.val_best = val_sorted[-1]
            self.run_id_best = id_sorted[-1]

            if len(pos_sorted)>=2:
                if abs(pos_sorted[-1]-pos_sorted[-2])<config.var_tolerance[config.var_names[self.cord]]:
                    complete = True
                    #print(f"Search along {cord} converged ! Two consecutive search parameters are within the tolerance. ")
                    
        
        return complete
