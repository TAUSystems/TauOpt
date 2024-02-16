""" Manange the job queue """

from ..config import *
import subprocess

def read_job_queue():
    """ 
    Find all jobs in the queue 

    Return:
        jobs (dict) : status of jobs currently in the queue

    """
    jobs = {}
    if config.username =='':
        out = subprocess.check_output(['echo'],shell=True)
    else:
        out = subprocess.check_output(['squeue','-u',config.username])
    
    out = out.decode('utf-8')
    lines = out.split('\n')

    for line in lines[1:]:
        if line.strip() !='':
            fields = line.split()
            if fields[4]=='PD':
                jobs[fields[0]]='PD'
            if fields[4]=='R':
                jobs[fields[0]]='R'
    
    return jobs   

def submit_job2q():
    """
    Submit a new job to the queue 
    
    """
    job_id=0

    jobs_inq = read_job_queue()
    njobs_inq = len(jobs_inq)

    if njobs_inq<config.max_num_jobs:

        try: 
        
            out = subprocess.check_output(['sbatch',config.submission_script])
                    
            out = out.decode('utf-8')
            lines = out.split('\n')

            #find the job ID for this submission
            for line in lines[1:]:
                if line.strip() !='':
                    fields = line.split()
                    if fields[0] == 'Submitted':
                        job_id = fields[3]
        
        except:
            pass
        
    else: 
        print(f"Can't submit another job 2 q. There are already {njobs_inq} jobs waiting/running in the q.")

    return job_id    