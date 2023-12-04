""" File and folder management (read, copy, delete) """
import os
import re
import shutil
import sys
from ..config import *
from ..run_sim import sim_status


def find_last_run(config):
    """ 
    find the last run folder in project_folder from any previous executions 
    
    Returns :
         int : the run number of the last run found by scanning project_folder   
    
    """

    # Get a list of all subfolders in the parent folder 
    subfolders = [f for f in os.listdir(config.project_folder) if os.path.isdir(os.path.join(config.project_folder, f))] 

    # Filter out subfolders that don't match the naming convention of "run$number" 
    subfolders = [f for f in subfolders if f.startswith('run') and f[3:].isdigit()] 

    # Sort the subfolders based on their number in descending order (highest number first) 
    subfolders.sort(key=lambda x: int(x[3:]), reverse=True) 

    # Get the path to the subfolder with the highest number 
    if subfolders: 
        find_num = re.findall('\d+$',subfolders[0])
        run_num = int(find_num[0]) 
        if not sim_status.sim_finished(run_num):
            run_num = run_num-1 
    else:
        print("Folders are named as run$run_num, where $run_num is a positive integer.") 
        print("No subfolders matching the naming convention were found. Starting from run1 . \n")    
        run_num = 0 

    return run_num




def copy_files(sim_num):

    """
    Copy all necessary files into the run folder
    Parameter: 
        sim_num (int) : current simulation number

    """

    dest_folder= os.path.join(config.project_folder, 'run'+str(sim_num)) 
    
    if not os.path.isfile(dest_folder+'/'+config.exec_name):

        #delete the existing dest_folder, if exists
        if os.path.isdir(dest_folder):
            shutil.rmtree(dest_folder)

        os.mkdir(dest_folder)
        os.mkdir(dest_folder+'/tau_opt')

        #copy the source code if the executable does not exist
        if not os.path.isfile(config.project_folder+'/'+config.code_name+'/'+config.exec_name):
            
            #copy the entire source code 
            print(f"Copying the source code to {dest_folder}\n")
            shutil.copytree(config.project_folder+'/'+config.code_name,dest_folder,dirs_exist_ok=True)
        
        else:
            #copy the executable if it does not contain '/'
            #if the exec_name contains '/', it would run from its current location, so not copying
            if '/' not in config.exec_name:
                shutil.copy(config.project_folder+'/'+config.code_name+'/'+config.exec_name,dest_folder)
            
            #copy the input files
            for n in range(len(config.input_files)):
                shutil.copy(config.project_folder+'/'+config.code_name+'/'+config.input_files[n],dest_folder)


        #copy all auxiliary files
        for n in range(len(config.aux_files)):
            shutil.copy(config.project_folder+'/'+config.code_name+'/'+config.aux_files[n],dest_folder)



        #copy the submission script, if needed
        if config.username!='':
            src_file = config.project_folder+'/'+config.code_name+'/'+config.submission_script
            if os.path.isfile(src_file):
                shutil.copy(src_file,dest_folder)
            else:
                sys.exit(f"username != '' means submission to the queue, but the submission script was not found in the code folder.")
    

