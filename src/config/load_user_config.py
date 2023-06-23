
""" Override the default configuration in config.py  """
import sys

def load_config(config,user_config,user_config_fname):
    """
    config            : the module containing all configuration variables

    user_config       : the (input) module that contain only the use-specific configuration varaibles 

    user_config_fname : name of the use-specific configuration file
    """
    
    print(f"---------------------------------------------------------- \n")
    print(f" Loading configuration from {user_config_fname}.py \n")
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

    if hasattr(user_config,"input_file"):
        config.input_file = user_config.input_file
    else:
        print(f" WARNING ! The list of files where input variables are searched/replaced ( input_file ) is not found in the config. file")

    if hasattr(user_config,"var_names"):
        config.var_names = user_config.var_names
    else:
        print(f" WARNING ! The list of input variables that are searched/replaced ( var_names ) is not found in the config. file")

    if hasattr(user_config,"var_names_prefix"):
        config.var_names_prefix = user_config.var_names_prefix
    
    if hasattr(user_config,"scan_type"):
        config.scan_type = user_config.scan_type
    
    
    """ 
    Optimization configuration 
    """
    
    if hasattr(user_config,"var_val0"):
        config.var_val0 = user_config.var_val0
        if not hasattr(user_config,"scan_type"):
            config.scan_type = 'opt'  # if var0 is provided, scan_type is set to 'opt' if not already set

    if hasattr(user_config,"var_range"):
        config.var_range = user_config.var_range

    if hasattr(user_config,"var_range"):
        config.var_range = user_config.var_range  



    """ 
    Configuration for other scan types 
    """
    #read input parameters from a file
    if hasattr(user_config,"var_filename"):
        if len(user_config.var_filename) !=0 :
            config.var_filename = user_config.var_filename
            if not hasattr(user_config,"scan_type"):
                config.scan_type = 'file' # if a valid var_filename is provided, scan_type is set to 'file' if not already set

    #get input parameters from a function
    if hasattr(user_config,"var_func"):
        if callable(user_config.var_func):
            config.var_func = user_config.var_func
            if not hasattr(user_config,"scan_type"):
                config.scan_type = 'func' # if a valid func is provided, scan_type is set to 'func' if not already set



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
    
    if hasattr(user_config,"max_num_jobs"):
        config.max_num_jobs = user_config.max_num_jobs


    """ Dictionaries with set of parameters  """

    if hasattr(user_config,"finished_sucessfully_if_exists"):
        config.finished_sucessfully_if_exists = user_config.finished_sucessfully_if_exists


    """ Set function pointers """

    if hasattr(user_config,"finished_sucessfully"):
         if callable(user_config.finished_sucessfully):
             config.finished_sucessfully = user_config.finished_sucessfully
    
    if hasattr(user_config,"objective_function"):
         if callable(user_config.objective_function):
             config.objective_function = user_config.objective_function
