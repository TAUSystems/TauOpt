import json

#full path of the project folder 
project_folder='/Users/rahul/Dropbox/TauOpt/examples/test_project'
#-----------------------------------------------------------------------------------------------
# code description
#-----------------------------------------------------------------------------------------------
code_name = 'test_code'
exec_name = 'test_code'
input_file = ["input.txt"]

#-----------------------------------------------------------------------------------------------
# parameters that change from run to run
#-----------------------------------------------------------------------------------------------

scan_type = 'opt' # func : predefined function; opt : optimization; file: read from a file

var_names = ['x1','x2']#['x1','x2','x3']
var_val0 = [3, 8] # initial value of the varaibles
var_range = {'x1':[1, 10], 'x2':[1, 10]}
tolerance = {'x1': 0.1, 'x2': 0.1}

#reading values of 'var_names' from a file
#var_filename = 'test_param.txt'


finished_sucessfully = { 'Folder'   : '' , 
                         'FileName' : 'output.txt' }


objective_function = 'output.txt'