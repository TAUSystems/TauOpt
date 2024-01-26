
""" Override the default configuration in config.py  """
import sys
from functools import reduce



def load_config(config,user_config,user_config_fname):
    """
    config            : the module containing all configuration variables

    user_config       : the (input) module that contain only the use-specific configuration varaibles 

    user_config_fname : name of the use-specific configuration file
    """
    
    print(f"---------------------------------------------------------- \n")
    print(f" Loading configuration from {user_config_fname} \n")
    print(f"----------------------------------------------------------\n")


    #if the config. varaible exists in the user config. file, override the values in the main config. file
    if hasattr(user_config,"project_folder"):
        config.project_folder = user_config.project_folder
    else:
        sys.exit("The absolute path of the project (project_folder) is not defined in the config file.")

    if hasattr(user_config,"code_name"):
        config.code_name = user_config.code_name
    else:
        sys.exit("Name of the code (code_name) is not defined in the config file.")

    if hasattr(user_config,"exec_name"):
        config.exec_name = user_config.exec_name
    else:
        config.exec_name = user_config.code_name #default, if the exec_name is not provided

    if hasattr(user_config,"input_files"):
        config.input_files = user_config.input_files
    #else:
    #    print(f" WARNING ! The list of files where input variables are searched/replaced ( input_file ) is not found in the config. file")

    if hasattr(user_config,"aux_files"):
        config.aux_files = user_config.aux_files 


    if hasattr(user_config,"var_names"):
        config.var_names = user_config.var_names
    #else:
    #    print(f" WARNING ! The list of input variables that are searched/replaced ( var_names ) is not found in the config. file")

    if hasattr(user_config,"var_names_prefix"):
        config.var_names_prefix = user_config.var_names_prefix
    
    
    """
    Set the scan type (default is 'opt')
    """
    
    if hasattr(user_config,"scan_type"):
        config.scan_type = user_config.scan_type
    else:
        if hasattr(user_config,"var_filename"):
            config.scan_type = 'file' # if var_filename is provided, scan_type is set to 'file'
        
        if hasattr(user_config,"var_func"):
            if callable(user_config.var_func):
                config.scan_type = 'func' # if a valid func is provided, scan_type is set to 'func' 
            else:
                print("Error :: 'var_func' in the config. file must be a callable python function.")
        
        if hasattr(user_config,"var_grid_npoints"): 
            config.scan_type = 'grid'

    
    
    """
    Optimization algorithm configuration
    """

    if config.scan_type == 'opt':

        required_user_config_var(config, user_config, "var_val0")
        required_user_config_var(config, user_config, "var_range")
        required_user_config_var(config, user_config, "var_tolerance")

        if hasattr(user_config,"opt_algo_config"):
            update_from_user_defined_dict( config.opt_algo_config , user_config.opt_algo_config)
            
        if hasattr(user_config,"model_poly_config"):
            update_from_user_defined_dict( config.model_poly_config , user_config.model_poly_config)

        if hasattr(user_config,"model_gp_config"):
            update_from_user_defined_dict( config.model_gp_config , user_config.model_gp_config)





    """ 
    Configuration for the other scan types 
    """
    #read input parameters from a file
    if config.scan_type == 'file':
        required_user_config_var(config, user_config, "var_filename")
        config.var_filename = user_config.var_filename

    #get input parameters from a function
    if config.scan_type == 'func':
        required_user_config_var(config, user_config, "var_func")
        config.var_func = user_config.var_func


    #generate input parameters for sampling
    if config.scan_type == 'grid':

        required_user_config_var(config, user_config, "var_range")
        
        set_var_dict_default_values(config.var_names, config.var_grid_npoints, 2)
        set_var_dict_default_values(config.var_names, config.var_grid_spacing, 'linear')
        
        if hasattr(user_config,"var_grid_npoints"):
            update_from_user_defined_dict( config.var_grid_npoints , user_config.var_grid_npoints)
        if hasattr(user_config,"var_grid_spacing"):    
            update_from_user_defined_dict( config.var_grid_spacing , user_config.var_grid_spacing)
        
    
    if config.scan_type == 'random':
        required_user_config_var(user_config, "var_range")


    """ 
    Code execution configuration 
    """

    if hasattr(user_config,"username"):
        config.username = user_config.username
        if hasattr(user_config,"submission_script"):
            config.submission_script = user_config.submission_script
        else:
            print(f" The name of job submission script is not found in the config. file. ")

    if hasattr(user_config,"local_exec_cmd"):
        config.local_exec_cmd = user_config.local_exec_cmd  

    if hasattr(user_config,"max_num_runs"):
        config.max_num_runs = user_config.max_num_runs
    
    if config.scan_type == 'grid':
        #max. num. of runs is set to the number of grid points
        config.max_num_runs = reduce(lambda x, y: x * y, config.var_grid_npoints.values())
    
    if hasattr(user_config,"max_num_jobs"):
        config.max_num_jobs = user_config.max_num_jobs



    """ 
    Function pointers / Dictionaries that define interaction with the source code
    """

    if hasattr(user_config,"finished_successfully"):
         config.finished_successfully = user_config.finished_successfully
    else: 
        config.finished_successfully = True
    
    if hasattr(user_config,"objective_function"):
         config.objective_function = user_config.objective_function
    
    if hasattr(user_config,"compile_source_code"):
        config.compile_source_code = user_config.commpile_source_code
    
    if hasattr(user_config,"restart"):
        config.restart = user_config.restart



    
    """
    Compilation configuration
    """

    if hasattr(user_config,"standard_compilation"):
        config.standard_compilation = user_config.standard_compilation

    """
    Additional configuration
    """
    if hasattr(user_config,"sleep_time"):
        config.sleep_time = user_config.sleep_time



def update_from_user_defined_dict( default_dict , user_dict):
    """
    Read dictionary (set of prameters) from the user config. file 
    and update the default dictionary defined in config.py
    """

    for v in default_dict:
        if v in user_dict:
            default_dict[v] = user_dict[v]


def set_var_dict_default_values(var_names, prop_dict, val):
    """
    Set default values in the dictionaries related to 'var_names'
    """
    for v in var_names:
        prop_dict[v] = val


def required_user_config_var(config, user_config, config_name ):
    """
    Check if the configuration variable is set in the user config. file
    """
    if not hasattr(user_config, config_name):
        print(f" Error :: '{config_name}' must be set in the user config. file")
    else:
        setattr(config, config_name, getattr(user_config, config_name) )