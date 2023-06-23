""" Polynomial : surrogate model for 1D data """
import numpy as np 
import scipy.optimize as scipy_opt

class ModelPoly:
        
    def __init__(self, max_deg=4) -> None:

        #4th order polynomial by default 
        self.max_deg = max_deg

    def acq_next_param(self, pos, val, lb, rb, tol):
        """
        Acquisition, get next point to evalaute the objective function
        
        Parameters: 
            pos (Numpy 1D array) : array of positions in current search
            val (Numpy 1D array) : corresponding values of the objective function
            lb, rb (float)       : left, right bounds for the position 
            tol (float)          : tolerance in determining pos, used in searching the max. of polynomial
        
        Returns : 
            next_pos (float) : position for the next evalaution of the objective function    
        
        """

        if len(pos) == 1:
            next_pos = pos[0] + (rb-lb)*0.25
            if next_pos>rb:
                next_pos =  pos[0] - (rb-lb)*0.5
        
        if len(pos) == 2:
            next_pos = pos[1] - (rb-lb)*0.25
            if next_pos < lb:
                 next_pos = pos[1] + (rb-lb)*0.5
        
        #use polynomials of degrees upto "max_deg" to determine the next pos. 
        if len(pos)>=3 :
            next_pos = self._max_poly(pos,val,lb,rb,tol) 

        return next_pos
    
    def _max_poly(self, pos, val, lb, rb, tol_pos):
        """
        Fit/train a polynomial to the existing points (pos, val) 
        Return the position corresponding to the max. of polynomial for next search 
        
        """

        degree = min(self.max_deg,len(pos)-1)
        neg_val = -val #negative values are used to find max. instead of min. returned by the scipy method used below                             
        coeff = np.polyfit(pos, neg_val, degree)

        poly = np.poly1d(coeff)
        
        #res = scipy_opt.minimize_scalar(poly, bounds=(code.var_range[var][0],code.var_range[var][1]), method='bounded')
        #return res.x

        res = scipy_opt.differential_evolution(poly, [( lb, rb)], atol=tol_pos*0.01, tol= 0)
        return res.x[0]



