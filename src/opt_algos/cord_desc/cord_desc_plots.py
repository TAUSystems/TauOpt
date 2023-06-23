""" Make plots showing progress """
from ...config import *
from . import cord_desc_utils as utils
from ...util import gbl_vars
import numpy as np
import os
import matplotlib.pyplot as plt


def plot_fval(run_info,sim_num, cord0):
    """
    Make plots for each simulation showing progress 

    """
    
    if not os.path.exists(config.project_folder+'/opt_plots'):
        os.mkdir(config.project_folder+'/opt_plots')
    
    print(f"Generating plot for Simulation Number {sim_num}...")
    
    fig = plt.figure()
    fig.suptitle(f"Coordinate Descent Optimization")
    
    ind = sim_num
    cord = cord0
    nscan = np.zeros(len(config.var_names),dtype=int)-1
    
    #determine scan number for each cont. run
    while ind>=1:
        pos,val,ind = utils.gather_cord_cont_runs(run_info,ind,cord)
        nscan[cord] = nscan[cord] + 1
        
        cord = cord - 1
        if cord ==-1:
            cord = len(config.var_names)-1
    
    
    ind = sim_num
    cord = cord0
    show_poly_fit = True
    #plot data points
    while ind>=1:
        pos,val,ind = utils.gather_cord_cont_runs(run_info,ind,cord)
        
    
        ax = plt.subplot(2,len(config.var_names),cord+1)
        
        # show individual simulation result as data points
        ax.plot(pos,val,'o',markersize=8, color=gbl_vars.colors[nscan[cord]],zorder=nscan[cord])
        plt.xlabel(config.var_names[cord])
        plt.xlim([config.var_range[config.var_names[cord]][0], config.var_range[config.var_names[cord]][1] ])
        
        #show the ploynomial fit for the very last scan
        if show_poly_fit:
            
            degree = min(4,len(pos)-1)
            coeff = np.polyfit(pos, val, degree)                   
            poly = np.poly1d(coeff)
            x = np.linspace( config.var_range[config.var_names[cord]][0], config.var_range[config.var_names[cord]][1], 100 )
            y = poly(x)
            ax.plot(x,y)
            show_poly_fit = False
    
        
        nscan[cord] = nscan[cord] - 1
        
        cord = cord - 1
        if cord ==-1:
            cord = len(config.var_names)-1
    
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
    plt.title(f"Max. value obtained in Simulation Number  {max_val_ind+1}")
    
    filename=config.project_folder+'/opt_plots/'+str(sim_num)+'.png'
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)
