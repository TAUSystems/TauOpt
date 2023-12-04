import sys
import os
import importlib.util
from src.config import * 
from src.io import *
from src.init import *
from src.util import *
from src.run_sim import *
from src.opt_algos import *



if __name__ == '__main__':
    
    #startup message
    start.startup_message()


    
    #load the user setup/configuration file as module
    try:
        
        user_config_fname, user_config_path = parse_input.user_config_file_name(sys.argv[1])
        user_config_spec = importlib.util.spec_from_file_location( user_config_fname, user_config_path)
        user_config = importlib.util.module_from_spec( user_config_spec )
        user_config_spec.loader.exec_module( user_config )
        load_user_config.load_config(config, user_config, user_config_fname)

    except:

        print(f"\n Could not load the user-defined configuration file.")
        sys.exit(f"The name of configuration file must be passed as an argument to TauOpt.py")

    
    #check the current configuration for any error
    check_config.check_all(config)
    start.check_all()

    #initialize local variables 
    finished = False
    sim_num = file_utils.find_last_run(config) #integer, last simulation number 

    #initialize all global variables
    start.init(config, gbl_vars, sim_num)

    #display startup completion message
    start.init_complete_message()

    #next simulation number
    sim_num = sim_num +1

    # check "all complete" status (could be complete if restarted) before moving further 
    if checks.all_complete(sim_num-1,gbl_vars.run_info):
        finished = True

    #wait/run/evalaute simulations in a loop
    while not finished:

        sleep_this_cycle = False

        if sim_num<=config.max_num_runs:

            """ 
            Get input parameters for next simulation ( simulation number  "sim_num") 
            
            """
            #determine from the configured optimization algorithm
            if config.scan_type=='opt':
                opt_algo.get_param(sim_num, gbl_vars.run_info)

            #read from a file    
            if config.scan_type=='file':
                read_params.read_param_from_file(sim_num,gbl_vars.run_info)
            
            #from a user defined function
            if config.scan_type=='func':
                read_params.func_param(sim_num,gbl_vars.run_info)
            
            #determined new parameters based on a scan-strategy
            if config.scan_type == 'grid' or config.scan_type == 'random' :
                read_params.auto_scan_param(sim_num,gbl_vars.run_info)
             


            """ 
            Process simulation number "sim_num" if a valid set of parameters is found
            
            """
            if checks.valid_param(sim_num):



                file_utils.copy_files(sim_num)

                #save parameters in a JSON file
                save_data.write_param(sim_num)
                                                    
                #repalce the variable $var_names with actual numbers
                write_inputs.write_new_param_into_setup_file(sim_num)
            
                sim_launcher.compile_and_run(sim_num)

                if sim_status.sim_submitted(sim_num):
                    sim_num = sim_num +1
                else:
                    print(f"Simulation Number {sim_num} could not be run/submitted.\n")
                    sleep_this_cycle= True #job was not submitted successfully. Try again.
            
            else:
                sleep_this_cycle = True
                print(f"No valid parameters for Simulation Number {sim_num} found ! ")
                
        
        #check status of every unfinished simulation
        checks.all_status_check(sim_num-1)

        
        #update plots and values of the objective function
        if config.scan_type == 'opt':
            opt_algo.update_run_info(sim_num-1,gbl_vars.run_info)


        #stop or continue ?   
        if checks.all_complete(sim_num-1,gbl_vars.run_info):
            finished = True
        else:
            sleep_this_cycle= True
            print(f"Time : {fmt.get_time()} . Going to sleep for {sleep_time} sec. \n")
            print(f"==========================================================================\n\n")


    #change dir to the project folder
    os.chdir(config.project_folder)

    #the final message before exiting this script
    if config.scan_type=='opt':
        disp_message.disp_best_sim_params(sim_num-1, run_info)

    print(f"\n==========================================================================")
    print(f" TauOpt finished at : {fmt.get_time()}")
    print(f"==========================================================================")  


