""" Make plots showing progress """
from ...config import *
from . import cord_desc_scans as utils
from ...util import gbl_vars
import numpy as np
import os
import matplotlib.pyplot as plt


def plot_fval(run_info,sim_num, scans, model):
    """
    Make plots for each simulation showing progress 

    """
    
    if not os.path.exists(os.path.join(config.project_folder, 'opt_plots')):

        os.mkdir(os.path.join(config.project_folder, 'opt_plots'))


    
    print(f"Generating plot for Simulation Number {sim_num}...")
    
    fig = plt.figure()
    fig.suptitle(f"Coordinate Descent Optimization")
    
    nscan = np.zeros(len(config.var_names), dtype = int) 
    
    #plot data points and model fit
    for n in range(1,scans.nscan+1):
        
        cord = scans.cord_scan[n].cord
        
        #update pos, val for the current scan
        if n == scans.nscan:
            scans.cord_scan[n].update_pos_val(run_info)

        pos = scans.cord_scan[n].pos
        val = scans.cord_scan[n].val
        
    
        ax = plt.subplot(2,len(config.var_names), cord+1)
        
        # show individual simulation result as data points
        markersize_ = 8
        if n < scans.nscan+1:
            markersize_ = 4

        ax.plot(pos,val,'o',markersize=markersize_, color=gbl_vars.colors[nscan[cord]], zorder=nscan[cord])
        plt.xlabel(config.var_names[cord])
        plt.xlim([config.var_range[config.var_names[cord]][0], config.var_range[config.var_names[cord]][1] ])

        
        #x-points where y is evaluated for plotting using the model
        x = np.linspace( config.var_range[config.var_names[cord]][0], config.var_range[config.var_names[cord]][1], 100 )
        
        #show the ploynomial fit for the current scan
        if config.opt_algo_config['model'] == 'poly' and n == scans.nscan :
            
            degree = min(config.model_poly_config['max_deg'],len(pos)-1)
            coeff = np.polyfit(pos, val, degree)                   
            poly = np.poly1d(coeff)
            y = poly(x)
            ax.plot(x,y)
        
        #show the GP model fit for the current scan
        if config.opt_algo_config['model'] == 'gp' and n == scans.nscan:

            if len(pos) > config.opt_algo_config['num_warm_points']:
                
                x_gp = x.reshape(-1,1)
                x_gp = model.X_scaler.transform(x_gp)
                
                # get mean and std from the GP model
                y, std = model.model.predict(x_gp, return_std = True) 
                y = y.reshape(-1,1)
                y = model.y_scaler.inverse_transform(y)
                y = y.ravel()
                std = std.ravel() * model.y_scaler.scale_

                ax.plot(x,y)
                plt.fill_between( x , y - 1.96 * std, y + 1.96 * std, alpha=0.2)

        #highlight the point for the current run sim_num
        if n == scans.nscan:
            ax.plot(pos[-1], val[-1], 'o' ,markersize=8 ,color='k', zorder=nscan[cord])


        
        nscan[cord] = nscan[cord] +1

    
    
    #histogram showing func values for all simulations
    pos = np.zeros(sim_num)
    val = np.zeros(sim_num)
    
    for n in range(1,sim_num+1):
        pos[n-1] = n
        val[n-1] = run_info['run'+str(n)]['opt_fval']
    
    max_val_ind = np.argmax(val)

    ax = plt.subplot(3,1,3)    
    bars = ax.bar(pos,val)
    bars[max_val_ind].set_color('red') 
    plt.xlabel("Simulation No.")
    plt.title(f"Max. value found in Simulation Number  {max_val_ind+1}")
    
    filename = os.path.join(config.project_folder, 'opt_plots', str(sim_num) + '.png')
    
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)
