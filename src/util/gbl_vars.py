""" Global varaibles used internally in TauOpt  """

#TauOpt will sleep for sleep_time seconds before attemping to run next simulation
sleep_time = 1

# stores important details for every run
run_info = {}

#colors for curves in plots
colors = ['r','g','b','c','m','y','r','g','b','c','m', 'y']

#stores reference of the algorithm instance
algo=''


"""
Copied/reorganized varaibles from config. or user-provided config. 
"""
#bounds of all variables
bounds = [(None , None)]

#tolerance for each input variable
tol = []

