""" Compile and run simuations """

from ..config import *
from . import sim_status
from . import job_queue
import os
import subprocess

def compile_and_run(sim_num):
    """
    compile and run simuation number sim_num

    """
    #compile the source code
    sim_compile(sim_num)

    #run the executable
    sim_run(sim_num)

def restart(sim_num): 
    """
    Restart the simulation
    """
    run_folder = os.path.join(config.project_folder, 'run'+str(sim_num))
    os.chdir(run_folder)

    try: 
        
        # call user-defined function to complete steps required for restart
        # if the function is not defined, it is assumned that simply running the executable 
        # will restart the simulation
        if callable (config.restart): 
            config.restart()
        
        sim_run(sim_num)
    
    except: 
        print(f"Error in restarting Simulation Number {sim_num}")
    


    os.chdir(config.project_folder)



def sim_compile(sim_num):
    """
    Compile the source code, if needed
    
    """

    run_folder = os.path.join(config.project_folder, 'run'+str(sim_num))
    os.chdir(run_folder)
     
    #compile the source code
    if not os.path.isfile(config.exec_name): 
        
        print(f"Compiling {config.code_name} in {run_folder}  \n")
        
        if callable(config.compile_source_code):
            try:
                config.compile_source_code(run_folder)
            except:
                print(f"The source code could not be compiles with user-defined method 'compile_source_code' ")
        else:
            
            #User did not provide any function for the compilation step
            #Try to compile the source code following standard procedure
            
            
            if os.path.isfile('Makefile'):
                try:
                    print(f"Using 'Makefile' to compile the source code")
                    subprocess.check_output([ 'make', 'clean' ]) 
                    subprocess.check_output([ 'make' ]) 
                except:
                    print(f"Could not compile the source code using 'Makefile' ")
            else:

                try:

                    simple_compilation(run_folder)
                
                except:
                    print(f" Failed to compile the source code with the simplest method !")
                    print(f" Compilation options: ")
                    print(f" a) provide a function 'compile_source_code' in the configuration file ")
                    print(f" b) Create a 'Makefile' in the code directory ")
                    print(f" c) if it is a simple (c/c++/fortran) code, TauOpt will try to compile the source \n") 
                    print(f"    code with 'standard_compilation' options defined in src/config/config.py  " )

    #else:
        #print(f"Executable already exists in {run_folder}, skipping compilation.")
    
    os.chdir(config.project_folder)


def sim_submit(sim_num):
    """
    Determine if the simulation number sim_num should be submitted/run
    Returns:
        submit (bool) : whether to (re)run or not 

    """
    
    #conditions for (re)submitting the simulation
    submit = False
    if not sim_status.sim_submitted(sim_num):
        submit = True
    else:
        if sim_status.sim_is_inq(sim_num):
            print(f"A job for run no. {sim_num} is already in the queue !! ") 
        else:
            if not sim_status.sim_finished(sim_num):
                submit = True
    
    return submit

def sim_run(sim_num):
    """
    Run locally or submit to the queue
    
    """

    submit = sim_submit(sim_num)
    os.chdir(os.path.join(config.project_folder, 'run'+str(sim_num)))


    job_id = 0                                          
    if submit:
#TODO This need to be changed the following to be compatible with Windows OS.        
        if config.username == '':

            print(f"Running Simulation Number  {sim_num}")            
            if len(config.local_exec_cmd)== 0:
                if '/' in config.exec_name:
                    subprocess.check_output([ config.exec_name ])
                else:
                    subprocess.check_output([ './'+config.exec_name ])
            else:
                subprocess.check_output(config.local_exec_cmd) 
            job_id=str(sim_num)
        
        else:
            print(f"Submitting Sumulation Number  {sim_num}")
            job_id=job_queue.submit_job2q()      
        
        if job_id !=0:
            #save/write the job ID in a text file
            with open(os.path.join('tau_opt', 'submitted_jobs.txt'), 'a') as f:
                f.write(job_id+'\n')
        else:
            print(f"sim. num. {sim_num} could not be executed or submitted to the queue.")
    
    os.chdir(config.project_folder)


#Follow standard procedure to compile simple source codes
def simple_compilation(run_folder):

    #list all files in the run folder
    src_files = [file for file in os.listdir(run_folder) ]

    obj_files = []
    ext = ''
    for src_file in src_files:
        
        ext = os.path.splitext(src_file)[1]
        
        if ext in config.standard_compilation:
        
            obj_file = f"{os.path.splitext(src_file)[0]}.o"
            obj_files.append(obj_file) 
            cmd = f"{config.standard_compilation[ext]} -c {os.path.join(run_folder,src_file)} "
            subprocess.run(cmd, shell=True) 

    if len(obj_file) !=0:
        try: 
            link_cmd = f"{config.standard_compilation[ext]} {' '.join(obj_files)} -o {config.exec_name}" 
            subprocess.run(link_cmd,shell=True)
        except:
            print(f"Failed to link the objects using simple/default compilation method.")