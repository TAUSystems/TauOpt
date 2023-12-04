""" Check simulation status and act """
from ..config import *
import os
from . import job_queue
from . import sim_launcher


def check_sim_status(sim_num):
    """
    Check the status of simulation number sim_num
    """
    
    if not sim_submitted(sim_num):
        
        print(f"sim. num. {sim_num} was never submitted !! Submitting now..")
        sim_launcher.compile_and_run(sim_num)
    
    else:
        
        if sim_is_inq(sim_num):
            print(f"sim num {sim_num} was submitted but still waiting/running. ")
        else:
            if not sim_finished(sim_num):     
                print(f"sim num {sim_num} was submitted but did not finish. Resubmitting/Restarting ... ")
                sim_launcher.restart(sim_num)
    
    
    
def sim_submitted(sim_num):
    res = False
    if os.path.isfile(config.project_folder+'/'+'run'+str(sim_num)+'/tau_opt/submitted_jobs.txt'):
        res = True
    return res
    
    
def sim_is_inq(sim_num):
    inq = False
    
    #check if the job is actually in the queue
    jobID_file = config.project_folder+'/'+'run'+str(sim_num)+'/tau_opt/submitted_jobs.txt'
    if os.path.isfile(jobID_file):    
        jobs = job_queue.read_job_queue() 
        with open(jobID_file,'r') as f:
            for line in f:
                job_id = line.strip()
                if job_id in jobs: 
                    inq = True
                    print(f"sim no. {sim_num} is in the queue with job id: {job_id} , status: {jobs[job_id]} ")
    
    return inq



def sim_finished(sim_num):
    """
    Determine whether the simulation number "sim_num" finished sucessfully or not.
    
    The criteria of sucess is configured by users either by defining "finished_successfully" function in the 
    configuration file or setting appropriate config. varaibles/dict that are interpreted in the following

    Returns:
        res (bool) : True, if the simulation finished sucessfully 
        
    """

    res = False #default
    
    if callable(config.finished_successfully):
        
        res = False
        if config.finished_successfully(sim_num):
            res = True

    elif isinstance( config.finished_successfully, dict ):
             
        file_path = config.finished_successfully['Folder']
        file_path = file_path.strip(" /") #strip spaces and /
        if file_path !='':
            file_path = '/'+file_path+'/'

        if os.path.isfile( config.project_folder+'/'+'run'+str(sim_num) + '/' + file_path + config.finished_successfully['FileName'] ):
            res = True
    
    elif config.finished_successfully:
        res = True
    

    return res
