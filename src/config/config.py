"""
Configuration file for TauOpt

The following configuration variables determine overall behaviour of TauOpt

The values of these variables in this file determine the default behaviour of TauOpt
These values can be overridden by passing a user-created configuration file to TauOpt.py 
Example : " TauOpt.py --user_config.py " 

The user-created configuration file is also a python file which contains distinct values of the varaibles 
and function reference defined below 

"""


#Full/absolute path to the project folder
# "project_folder" directory contains the source code all files/folder produced by TauOpt
project_folder=''

# Name of the simulation code
# The source code must be within the directory  "project_folder/code_name/"  
code_name =''

#Name of the executable 
exec_name = ''

#list of all files that contain chaging "input variables" defined in var_names below
input_file = []

#list containing names of the all varaibles are the changed from one run to another.
#the files listed in "input_files" contain elements of var_names (with prefix "var_names_prefix") which are automatically replaced by
#a valid numeral value
#Example : var_names = ['x1','x2']
var_names = ['']

#This prefix is combined with elements of var_names to indetify strings that are replaced by numeral values
var_names_prefix = '$'

# scan_type defines how the input varaibles are changed
# 
# 'func' : get new set of varaibles from a user defined function
# 'opt'  : automatically adjust the values of input varaibles with optimization
# 'file' : read the values sequentially from a file
#
# each mode listed above requires additional configuration varaibles defined below

scan_type = ''



"""

Configuration for optimization

The values of "var_names" are varied automatically 

scan_type = 'opt'

"""

#list : initial values of the varaibles listed in "var_names"
#Example : var_val0 = [3, 8.2] 
var_val0 = [] 

#range of the varaibles, if the values are determined using an optimization algorithm 
#Example : var_range = {'x1':[1, 10], 'x2':[2.0, 10.0]}
var_range = {}

#tolerance in the determination of the optimal values 
var_tolerance = {'x1': 0.1, 'x2': 0.1, 'x3':0.1 }

#type of optimization algorithm
opt_algo_type = 'cord_desc'



"""

Configuration for sequential scan

The values of "var_names" are read from a file  

scan_type = 'file'

"""

#name of the file containing values of the variables
#supported formats/extensions : .txt, .csv, .xls, .xlsx, .h5, .hdf5
#Example : var_filename = 'test_param.txt'
var_filename = ''



"""

Configuration for sequential scan

The values of "var_names" are obtained from a user-defined function 

scan_type = 'func'

"""

var_func = ''





"""

Configuration for code execution, queue managment

"""

#name of the job submission script. The file must be located in "project_folder/code_name"
#Example : submission_script = 'pictor.slurm'
submission_script = ''

# username, if the simulations are run submitted to a queue manager (slurm, PBS) 
# Example : username = 'rahulkr'
# Default : username = '' implies running on the local computer 
username = ''

#command for the local execution
#Default : ./exec_name  
#Example : local_exec_cmd = ['mpirun','-np','4','./PICTOR']
local_exec_cmd = []

#maximum number of simulations run by TauOpt
max_num_runs = 100

#maximum number of jobs in the queue (waiting+running)
max_num_jobs = 10


"""

Dictionaries :: set of config. parameters that user can pass to configure some specific functions used internally

"""




"""

Function/Dictionaries for interacting with the simulation code

Note: functions defined in the config. files are called from the run folder (project_folder/run$sim_num)

"""


# Determine if the simulation finished sucessfully
# callable function, or 
# based on whether a file/folder exists or not
# Example : 
# finished_successfully = { 'Folder'    : 'data' # relative path (from project_folder/run$sim_num/) of the file that is looked for
#                           'FileName'  :  name of the file
#                        }

finished_successfully = None

#objective function whose output is optimized 
objective_function = None

#function detailing compilation steps 
compile_source_code = None 

"""
Configuration for compiling source codes
"""

# Default compilers to compile simple source codes
# Key: file extension, Value: compiler with flags/options
# To use different compilers/flags, define the 'standard_compilation' dict. in your configulation file to override the default here 
standard_compilation =   { '.c'   : 'gcc', 
                           '.cpp' : 'g++',
                           '.f90' : 'gfortran'
                         }
