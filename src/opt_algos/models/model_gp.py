""" Gaussian Process :: surrogate model for Bayesian optimization """
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from sklearn.preprocessing import StandardScaler
from scipy.optimize import differential_evolution
from scipy.stats import norm
import numpy as np

class ModelGP:

    def __init__(self) -> None:
        self.kernel = Matern(nu = 1.5)
        self.model = GaussianProcessRegressor(kernel=self.kernel, n_restarts_optimizer=10)
        
        self.best_x = None
        self.best_y = None

        self.X_scaler = StandardScaler()
        self.y_scaler = StandardScaler() 
        

    def acq_next_param(self, X, y, bounds , tol ):
        """
        Returns next point to evaluate the objective function
        """

        #scale the data
        X_scaled, y_scaled = self._scale_data(X,y)
        bounds_scaled =  self._scale_bounds(bounds)

        #fit GP model to the data
        self.model.fit( X_scaled, y_scaled )

        #update the best value
        self.best_x, self.best_y = self._best_observed(X_scaled,y_scaled)

        # last same point is the initial point for searching the minimum 
        tol = self.X_scaler.scale_
        abs_tol = 0.01*np.min(tol)
        pos_next = differential_evolution ( self._acq_func_ei , bounds_scaled , atol=abs_tol , tol= 0)


        pos_next = pos_next.x
        pos_next = np.atleast_2d(pos_next)
        pos_next = self.X_scaler.inverse_transform(pos_next)[0]
        print (pos_next)

        return pos_next
    

    def _scale_data(self, X,y):
        """
        Standard scaling of the training data
        """
        X_scaled = self.X_scaler.fit_transform(X)
        y_scaled = self.y_scaler.fit_transform(y)

        return X_scaled, y_scaled 
    
    
    def _scale_bounds(self, bounds):
        """
        Scale the boundaries
        """
        lb = [ t[0] for t in bounds ]
        rb = [ t[1] for t in bounds ] 

        lb = np.atleast_2d(lb)
        rb = np.atleast_2d(rb)

        lb_scaled = self.X_scaler.transform(lb)[0]
        rb_scaled = self.y_scaler.transform(rb)[0]

        bounds_scaled = [ (x,y) for x, y in zip(lb_scaled, rb_scaled)]
        
        return bounds_scaled 
    

    
    def _acq_func_ucb(self,x):
        """
        Acquisition Function :: Upper Confidence Bound
        """
        x = np.atleast_2d(x)
        mean, std = self.model.predict(x, return_std= True) 
    
        return -mean - 2.0 * std
    
    def _acq_func_ei(self,x):
        """
        Acquisition Function :: Expected Improvement
        """
        x = np.atleast_2d(x)
        mean, std = self.model.predict(x, return_std= True) 
        
        if std != 0:
            z = (mean - self.best_y ) / std
            ei = (mean - self.best_y ) * norm.cdf(z) + std * norm.pdf(z)
        else: 
            ei = 0

        return -ei
    

    def _best_observed(self, X , y):
        """
        Returns the best point observed so far
        """
        
        best_idx = np.argmax(y)
        return X[best_idx], y[best_idx]
