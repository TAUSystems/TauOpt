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



def sim_compile(sim_num):
    """
    Compile the source code, if needed
    
    """

    run_folder = config.project_folder+'/'+'run'+str(sim_num)
    os.chdir(run_folder)
     
    #compile the source code
    if not os.path.isfile(config.exec_name): 
        print(f"Compiling {config.code_name} in {run_folder}")
        config.compile_source_code(run_folder)
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
    os.chdir(config.project_folder+'/'+'run'+str(sim_num))

    job_id = 0                                          
    if submit:
        
        if config.username == '':
            print(f"Running Sumulation Number  {sim_num}")
            if config.local_exec_cmd=='':
                subprocess.check_output([ './', config.exec_name ])
            else:
                subprocess.check_output(config.local_exec_cmd) 
            job_id=str(sim_num)
        else:
            print(f"Submitting Sumulation Number  {sim_num}")
            job_id=job_queue.submit_job2q()      
        
        if job_id !=0:
            #save/write the job ID in a text file
            with open('tau_opt/submitted_jobs.txt','a') as f:
                f.write(job_id+'\n')
        else:
            print(f"sim. num. {sim_num} could not be executed or submitted to the queue.")
    
    os.chdir(config.project_folder)

